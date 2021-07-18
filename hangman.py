import os
from enum import Enum

PLACE_HOLDER = '_'


class Hangman:
    def __init__(self, word):
        self.word = word
        self.guesses = set()

    def guess(self, character):
        self.guesses.add(str.lower(character))

    def guess_word(self, guess):
        return str.lower(guess) == str.lower(self.word)

    def count_misses(self):
        return len(self.guesses-set(self.word))

    def count_open_letters(self):
        return self.status().count(PLACE_HOLDER)

    def status(self):
        return ''.join([self._make_visible(x) for x in self.word])

    def _make_visible(self, character):
        if str.lower(character) in self.guesses:
            return character
        else:
            return PLACE_HOLDER


class GameState(Enum):
    RUNNING = 0
    WON = 1
    LOST = -1


class HangmanGame:
    missed_word_guesses = 0
    word_guessed_correctly = False

    def __init__(self, word, allowed_misses=10):
        self.allowed_misses = allowed_misses
        self.hangman = Hangman(word)

    def guess(self, guess_input):
        if guess_input is None or guess_input == '':
            pass
        elif len(guess_input) == 1:
            self.hangman.guess(guess_input)
        else:
            self._guess_word(guess_input)

        return self.visual_state()

    def remaining_guesses(self):
        return self.allowed_misses - self.hangman.count_misses() - self.missed_word_guesses

    def _guess_word(self, word):
        self.word_guessed_correctly = self.hangman.guess_word(word)
        if not self.word_guessed_correctly:
            self.missed_word_guesses += 1

    def is_over(self):
        return self.hangman.count_open_letters() == 0 or self.remaining_guesses() <= 0 or self.word_guessed_correctly

    def state(self):
        if self.word_guessed_correctly or self.hangman.count_open_letters() == 0:
            return GameState.WON
        elif self.allowed_misses >= self.missed_word_guesses:
            return GameState.RUNNING
        else:
            return GameState.LOST

    def _visual_score(self):
        return ''.join(['O' if x < self.remaining_guesses() else 'Ø' for x in reversed(range(self.allowed_misses))])

    def visual_state(self):
        return f'{self.hangman.status()}\n{self._visual_score()}'


def play(word):
    clear_screen()
    game = HangmanGame(word)
    while game.state() == GameState.RUNNING:
        guess = input()
        state_visualisation = game.guess(guess)
        print(state_visualisation)

    if game.state() == GameState.WON:
        print('Gewonnen!')
    else:
        print('Versuch es noch einmal')


def clear_screen():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')
    # print out some text

