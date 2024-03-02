"""
Tests
"""

import unittest
import os

from linkedtext.linkedtext import LinkedText
from tests.string import string as markdown_string

from linkedtext.exceptions import (
    FileNotFound,
    ArgumentError,
    EmptyString,
    InvalidFile,
    EmptyMarkdown
)


class TestLinkedText(unittest.TestCase):

    BASE = 'tests'
    SAMPLE_ORIGIN = 'sample.md'
    SAMPLE_FINISHED = 'sample_finish.md'
    NOT_MARKDOWN = 'not_markdown.txt'
    EMPTY_MARKDOWN = 'empty.md'

    def setUp(self):
        self.origin = os.path.join(
                                    TestLinkedText.BASE,
                                    TestLinkedText.SAMPLE_ORIGIN
                                )
        self.finish = os.path.join(
                                    TestLinkedText.BASE,
                                    TestLinkedText.SAMPLE_FINISHED
                                )
        self.not_markdown = os.path.join(
                                    TestLinkedText.BASE,
                                    TestLinkedText.NOT_MARKDOWN
                                )
        self.markdown_empty = os.path.join(
                                    TestLinkedText.BASE,
                                    TestLinkedText.EMPTY_MARKDOWN
                                )

        self.string = markdown_string

    def read(
        self,
        filename: str
    ) -> list:
        data = []
        with open(filename, 'r') as fl:
            data = fl.readlines()
            return data

    def test_string_process(self):
        instance = LinkedText(markdown_file=self.origin)
        instance.process()
        data_file = self.read(self.finish)
        self.assertEqual(len(''.join(instance.data)), len(''.join(data_file)))

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

    def test_raise_emptyMarkdown(self):
        with self.assertRaises(EmptyMarkdown):
            c = LinkedText(markdown_file=self.markdown_empty, string=None)
            c.process()

    def test_raise_invalidFile(self):
        with self.assertRaises(InvalidFile):
            c = LinkedText(markdown_file=self.not_markdown, string=None)
            c.process()

    @classmethod
    def tearDown(cls):
        finish_path = os.path.join(
                                    TestLinkedText.BASE,
                                    TestLinkedText.SAMPLE_FINISHED
                                )
        if os.path.exists(finish_path):
            os.remove(finish_path)
