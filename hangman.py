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


class HangmanGame:
    missed_word_guesses = 0
    word_guessed_correctly = False

    def __init__(self, word, allowed_guesses=10):
        self.allowed_guesses = allowed_guesses
        self.hangman = Hangman(word)

    def guess(self, character):
        self.hangman.guess(character)

    def remaining_guesses(self):
        return self.allowed_guesses - self.hangman.count_misses() - self.missed_word_guesses

    def guess_word(self, word):
        self.word_guessed_correctly = self.hangman.guess_word(word)
        if not self.word_guessed_correctly:
            self.missed_word_guesses += 1
        return self.word_guessed_correctly

    def is_over(self):
        return self.hangman.count_open_letters() == 0 or self.remaining_guesses() <= 0 or self.word_guessed_correctly

