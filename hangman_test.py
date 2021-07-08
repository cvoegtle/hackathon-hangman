import unittest
from hangman import Hangman
from hangman import HangmanGame


class MyTestCase(unittest.TestCase):
    def test_initialStatus(self):
        hangman = Hangman("Hallo")
        self.assertEqual('_____', hangman.status())

    def test_wrong_guess(self):
        hangman = Hangman("Hello")
        hangman.guess('a')
        self.assertEqual('_____', hangman.status())

    def test_good_guess(self):
        hangman = Hangman("Hello")
        hangman.guess('e')
        self.assertEqual('_e___', hangman.status())
        hangman.guess('l')
        self.assertEqual('_ell_', hangman.status())

    def test_guess_case_insensitive(self):
        hangman = Hangman('Hello')
        hangman.guess('E')
        self.assertEqual('_e___', hangman.status())
        hangman.guess('h')
        self.assertEqual('He___', hangman.status())

    def test_count_misses(self):
        hangman = Hangman('Hello')
        hangman.guess('a')
        self.assertEqual(1, hangman.count_misses())
        hangman.guess('b')
        self.assertEqual(2, hangman.count_misses())
        hangman.guess('c')
        self.assertEqual(3, hangman.count_misses())
        hangman.guess('A')
        self.assertEqual(3, hangman.count_misses())
        self.assertEqual(set('abc'), hangman.guesses)

        hangman.guess('e')
        self.assertEqual(3, hangman.count_misses())

    def test_guess_word_miss(self):
        game = HangmanGame('Hello')
        guess_successful = game.guess_word('hallo')
        self.assertFalse(guess_successful)
        self.assertEqual(game.allowed_guesses-1, game.remaining_guesses())

    def test_guess_word_hit(self):
        game = HangmanGame('Hello')
        guess_successful = game.guess_word('hello')
        self.assertTrue(guess_successful)
        self.assertEqual(game.allowed_guesses, game.remaining_guesses())

    def test_remaining_guesses(self):
        game = HangmanGame('Hello')
        self.assertEqual(game.allowed_guesses, game.remaining_guesses())
        game.guess('e')
        self.assertEqual(game.allowed_guesses, game.remaining_guesses())
        game.guess('a')
        self.assertEqual(game.allowed_guesses-1, game.remaining_guesses())

    def test_game_over(self):
        game = HangmanGame('Hello')
        game.guess('e')
        self.assertFalse(game.is_over())
        game.guess('h')
        game.guess('l')
        game.guess('o')
        self.assertTrue(game.is_over())

    def test_game_over_word_guess(self):
        game = HangmanGame('Hello')
        game.guess_word('HELLO')
        self.assertTrue(game.is_over())

    def test_game_over_too_many_misses(self):
        game = HangmanGame('Hello', 5)
        game.guess('a')
        game.guess('b')
        game.guess('c')
        game.guess('d')
        self.assertFalse(game.is_over())
        game.guess('f')
        self.assertTrue(game.is_over())





if __name__ == '__main__':
    unittest.main()