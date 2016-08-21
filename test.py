"""
Test Module

Example:
    This module require Python3.4 to run. To execute this program run following
    command on terminal ::
    $ python3 test.py

Author : Rajat Mhetre

"""

import unittest
import os
from app import add_contact, Trie

DATA_URL = os.path.join(os.getcwd() + "/dummy_data.txt")


class TestCases(unittest.TestCase):
    """
            TestCases extended from unittest.TestCase Class
            Note:
            	Do not include the `self` parameter in the ``Args`` section.
    """

    def test_add_dummy_contacts(self):
        """
                Adds dummy names from file into trie
        """
        trie = Trie()
        with open(DATA_URL) as in_file:
            for line in in_file:
                self.assertTrue(add_contact(trie, line.strip()))


if __name__ == '__main__':
    unittest.main()
