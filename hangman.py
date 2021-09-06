import os
from enum import Enum
from getpass import getpass

PLATZ_HALTER = '_'


class Hangman:
    def __init__(self, wort):
        self.ziel_wort = wort
        self.geratene_buchstaben = set()

    def raten(self, tipp):
        self.geratene_buchstaben.add(str.lower(tipp))

    def wort_raten(self, ganzes_wort):
        return str.lower(ganzes_wort) == str.lower(self.ziel_wort)

    def fehler_zaehlen(self):
        return len(self.geratene_buchstaben - set(str.lower(self.ziel_wort)))

    def fehlende_buchstaben(self):
        return self.zustand().count(PLATZ_HALTER)

    def zustand(self):
        return ''.join([self._sichtbar_machen(x) for x in self.ziel_wort])

    def _sichtbar_machen(self, character):
        if str.lower(character) in self.geratene_buchstaben:
            return character
        else:
            return PLATZ_HALTER


class SpielStatus(Enum):
    LAUFEND = 0
    GEWONNEN = 1
    VERLOREN = -1


class HangmanSpiel:
    wort_rate_fehlschlaege = 0
    wort_erraten = False

    def __init__(self, wort, anzahl_erlaubter_fehler=10):
        self.anzahl_erlaubter_fehler = anzahl_erlaubter_fehler
        self.hangman = Hangman(wort)

    def raten(self, eingabe):
        if eingabe is None or eingabe == '':
            pass
        elif len(eingabe) == 1:
            self.hangman.raten(eingabe)
        else:
            self._wort_raten(eingabe)

        return self.status_als_text()

    def verbleibende_versuche(self):
        return self.anzahl_erlaubter_fehler - self.hangman.fehler_zaehlen() - self.wort_rate_fehlschlaege

    def _wort_raten(self, word):
        self.wort_erraten = self.hangman.wort_raten(word)
        if not self.wort_erraten:
            self.wort_rate_fehlschlaege += 1

    def beendet(self):
        return self.hangman.fehlende_buchstaben() == 0 or self.verbleibende_versuche() <= 0 or self.wort_erraten

    def status(self):
        if self.wort_erraten or self.hangman.fehlende_buchstaben() == 0:
            return SpielStatus.GEWONNEN
        elif self.verbleibende_versuche() > 0:
            return SpielStatus.LAUFEND
        else:
            return SpielStatus.VERLOREN

    def _spielstand_als_text(self):
        return ''.join(['O' if x < self.verbleibende_versuche() else 'Ø' for x in reversed(range(self.anzahl_erlaubter_fehler))])

    def status_als_text(self):
        return f'{self.hangman.zustand()}\n{self._spielstand_als_text()}'


def spielen(wort):
    spiel = HangmanSpiel(wort)
    print(spiel.status_als_text())
    while spiel.status() == SpielStatus.LAUFEND:
        eingabe = input('Dein Tipp:')
        spielstand_anzeige = spiel.raten(eingabe)
        print(spielstand_anzeige)

    if spiel.status() == SpielStatus.GEWONNEN:
        print('Gewonnen!')
    else:
        print(f'gesucht war {wort}. Versuch es noch einmal')


if __name__ == '__main__':
    wort = getpass('Gesuchtes Wort:')
    spielen(wort)
