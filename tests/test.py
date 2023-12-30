"""
Tests
"""

import unittest
import os

from linkedtext.linkedtext import LinkedText
from linkedtext.exceptions import FileNotFound


class TestLinkedText(unittest.TestCase):

    def setUp(self):
        self.path = 'tests'
        self.origin = self.path + '/sample.md'
        self.finish = self.path + '/sample_finish.md'
        self.cls = LinkedText(self.origin)

    def test_process(self):
        def read():
            data = []
            with open(self.finish, 'r') as fl:
                data = fl.readlines()
            return data
        self.cls.process()

        self.assertEqual(len(''.join(self.cls.data)), len(''.join(read())))

    def test_raise_fileNotFound(self):
        with self.assertRaises(FileNotFound):
            c = LinkedText()
            c.process()

    def tearDown(self):
        if os.path.exists(os.path.abspath(self.finish)):
            os.remove(os.path.abspath(self.finish))
