import unittest
from hangman import Hangman, SpielStatus
from hangman import HangmanSpiel


class MyTestCase(unittest.TestCase):
    def test_ausgangszustand(self):
        hangman = Hangman("Hallo")
        self.assertEqual('_____', hangman.zustand())

    def test_falscher_tipp(self):
        hangman = Hangman("Hello")
        hangman.raten('a')
        self.assertEqual('_____', hangman.zustand())

    def test_richtiger_tipp(self):
        hangman = Hangman("Hello")
        hangman.raten('e')
        self.assertEqual('_e___', hangman.zustand())
        hangman.raten('l')
        self.assertEqual('_ell_', hangman.zustand())

    def test_tips_grossschreibung_egal(self):
        hangman = Hangman('Hello')
        hangman.raten('E')
        self.assertEqual('_e___', hangman.zustand())
        hangman.raten('h')
        self.assertEqual('He___', hangman.zustand())

    def test_fehler_zaehlen(self):
        hangman = Hangman('Hello')
        hangman.raten('a')
        self.assertEqual(1, hangman.fehler_zaehlen())
        hangman.raten('b')
        self.assertEqual(2, hangman.fehler_zaehlen())
        hangman.raten('c')
        self.assertEqual(3, hangman.fehler_zaehlen())
        hangman.raten('A')
        self.assertEqual(3, hangman.fehler_zaehlen())
        self.assertEqual(set('abc'), hangman.geratene_buchstaben)
        hangman.raten('H')
        self.assertEqual(3, hangman.fehler_zaehlen())
        hangman.raten('e')
        self.assertEqual(3, hangman.fehler_zaehlen())

    def test_falsches_wort(self):
        spiel = HangmanSpiel('Hello')
        spiel.raten('hallo')
        state = spiel.status()
        self.assertEqual(SpielStatus.LAUFEND, state)
        self.assertEqual(spiel.anzahl_erlaubter_fehler - 1, spiel.verbleibende_versuche())

    def test_richtiges_wort(self):
        spiel = HangmanSpiel('Hello')
        richtiger_tipp = spiel.raten('hello')
        self.assertTrue(richtiger_tipp)
        self.assertEqual(spiel.anzahl_erlaubter_fehler, spiel.verbleibende_versuche())

    def test_verbleibende_versuche(self):
        spiel = HangmanSpiel('Hello')
        self.assertEqual(spiel.anzahl_erlaubter_fehler, spiel.verbleibende_versuche())
        spiel.raten('e')
        self.assertEqual(spiel.anzahl_erlaubter_fehler, spiel.verbleibende_versuche())
        spiel.raten('a')
        self.assertEqual(spiel.anzahl_erlaubter_fehler - 1, spiel.verbleibende_versuche())

    def test_spiel_zuende(self):
        spiel = HangmanSpiel('Hello')
        spiel.raten('e')
        self.assertFalse(spiel.beendet())
        spiel.raten('h')
        spiel.raten('l')
        spiel.raten('o')
        self.assertTrue(spiel.beendet())

    def test_spiel_vorbei_durch_geratene_worte(self):
        spiel = HangmanSpiel('Hello')
        spiel.raten('HELLO')
        self.assertTrue(spiel.beendet())

    def test_spiel_beendet_durch_falsche_buchstaben(self):
        spiel = HangmanSpiel('Hello', 5)
        spiel.raten('a')
        spiel.raten('b')
        spiel.raten('c')
        spiel.raten('d')
        self.assertFalse(spiel.beendet())
        spiel.raten('f')
        self.assertTrue(spiel.beendet())

    def test_spielstatus_laufend(self):
        spiel = HangmanSpiel('Hello', 5)
        self.assertEqual(SpielStatus.LAUFEND, spiel.status())

    def test_spielstatus_gewonnen(self):
        spiel = HangmanSpiel('Hello')
        spiel.raten('HELLO')
        self.assertEqual(SpielStatus.GEWONNEN, spiel.status())

    def test_gewonnen_durch_geratene_buchstaben(self):
        spiel = HangmanSpiel('you')
        spiel.raten('u')
        spiel.raten('y')
        spiel.raten('o')
        self.assertEqual(SpielStatus.GEWONNEN, spiel.status())

    def test_verloren_durch_geratene_buchstaben(self):
        spiel = HangmanSpiel('you', 3)
        spiel.raten('a')
        spiel.raten('b')
        spiel.raten('c')
        self.assertEqual(SpielStatus.VERLOREN, spiel.status())

    def test_spielstatus_verloren(self):
        spiel = HangmanSpiel('Hello', 1)
        self.assertEqual(SpielStatus.LAUFEND, spiel.status())
        spiel.raten('HELLa')
        self.assertEqual(SpielStatus.VERLOREN, spiel.status())

    def test_spielstatus_als_text(self):
        spiel = HangmanSpiel('Hello', 10)
        self.assertEqual('_____\nOOOOOOOOOO', spiel.status_als_text())

    def test_spiel_status_laufend(self):
        spiel = HangmanSpiel('Hello', 10)
        spiel.raten('a')
        self.assertEqual('_____\nØOOOOOOOOO', spiel.status_als_text())


if __name__ == '__main__':
    unittest.main()
