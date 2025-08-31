""" this is import section """

import unittest
import string_utils


class Teststring(unittest.TestCase):
    """this is where class build """


    def test_word(self):
        """this is were first capitalization sort out"""
        text = 'love'
        result = string_utils.capitalize_first_letter(text)
        self.assertEqual(result,'Love')


    def test_palandrom_check(self):
        """this is plandrom check happen"""
        word = 'dad'
        result = string_utils.is_palindrome(word)
        self.assertEqual(result,True)


if __name__ == '__main__':
    unittest.main()
