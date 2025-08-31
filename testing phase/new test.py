"""Unit tests for string_utils functions."""

import unittest
import string_utils


class TestString(unittest.TestCase):
    """Test cases for string utility functions."""

    def test_word(self):
        """Test if first letter is capitalized correctly."""
        text = 'love'
        result = string_utils.capitalize_first_letter(text)
        self.assertEqual(result, 'Love')

    def test_palindrome_check(self):
        """Test if word is detected as a palindrome."""
        word = 'dad'
        result = string_utils.is_palindrome(word)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

