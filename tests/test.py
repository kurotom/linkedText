"""
Tests
"""

import unittest
import os

from linkedtext.linkedtext import LinkedText
from tests.string import string

from linkedtext.exceptions import (
    FileNotFound,
    ArgumentError,
    EmptyString
)


class TestLinkedText(unittest.TestCase):

    def setUp(self):
        self.path = 'tests'
        self.origin = self.path + '/sample.md'
        self.finish = self.path + '/sample_finish.md'
        self.string = string

    def test_string_process(self):
        self.cls = LinkedText(markdown_file=self.origin)
        self.cls.process()
        self.assertGreater(len(self.cls.data), 0)

    def test_file_process(self):
        def read():
            data = []
            with open(self.finish, 'r') as fl:
                data = fl.readlines()
            return data
        self.cls = LinkedText(markdown_file=self.origin)
        self.cls.process()

        self.assertEqual(len(''.join(self.cls.data)), len(''.join(read())))

    def test_raise_argumentError(self):
        with self.assertRaises(ArgumentError):
            c = LinkedText()
            c.process()

    def test_raise_fileNotFound(self):
        with self.assertRaises(FileNotFound):
            c = LinkedText(markdown_file='ABC')
            c.process()

    def test_raise_stringEmpty(self):
        with self.assertRaises(EmptyString):
            c = LinkedText(string='')
            c.process()

    def tearDown(self):
        if os.path.exists(os.path.abspath(self.finish)):
            os.remove(os.path.abspath(self.finish))
