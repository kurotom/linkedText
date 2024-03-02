# -*- coding: utf-8 -*-
"""
Class to generate links and table of contents from a Markdown file, generating
a new final Markdown file with the links and table of contents generated.

The original file is never altered, the final or generated file ends with a
prefix `_finish`.

"""

from linkedtext.exceptions import (
    FileNotFound,
    ArgumentError,
    EmptyString,
    InvalidFile,
    EmptyMarkdown
)

from linkedtext.utils import (
    is_file,
    prepare_string
)

import re
import os


class LinkedText:
    """
    Class that generates table of contents and links.
    """

    PREFIX = '_finish'

    def __init__(
        self,
        markdown_file: str = None,
        string: str = None,
    ) -> None:
        """
        Constructor:

        Parameters:
            filename : str, name of file Markdown. Required.

        Return:
            None
        """
        self.filename = markdown_file
        self.string = string
        self.name = None
        self.extention = None
        self.data = []
        self.indexes = []
        self.contents_list = ''

    def __read(
        self,
        filename: str = None
    ) -> list:
        """
        Read data of file.

        Parameters:
            filename: str, Markdown file.

        Return:
            list: list of lines of file.
        """
        with open(filename, 'r') as fl:
            data = fl.readlines()
            if len(data) == 0:
                raise EmptyMarkdown()
            return data

    def __check_content(self) -> None:
        """
        Checks existence and content of the data source.

        Raises:
            `FileNotFound`: file markdown not found.
            `InvalidFile`: file provided is not a markdown file.
            `ArgumentError`: incorrect argument.
            `EmptyString` : empty string.
        """
        if self.filename is not None:
            if not os.path.exists(self.filename):
                raise FileNotFound('Need a file to start convert.')

            if is_file(self.filename):
                name_, extention_ = os.path.splitext(self.filename)
                if extention_.lower() != '.md':
                    raise InvalidFile(self.filename)

                self.data = self.__read(self.filename)
                self.name = name_
                self.extention = extention_
            else:
                raise InvalidFile(self.filename)

        elif self.string is not None:
            if isinstance(self.string, str):
                if len(self.string) > 0:
                    self.data = prepare_string(self.string)
                else:
                    raise EmptyString()
            else:
                raise ArgumentError('Parameter "string" must be a string.')
        else:
            raise ArgumentError()

    def process(
        self
    ) -> None:
        """
        Main function to process list of lines of file Markdown.
        Iterates over a list of lines, generates links, inserts data into the
        list, calls generate a table of contents, and calls write to a file.

        Returns:
            None
        """

        self.__check_content()

        list_indexes = self.get_indexes()

        index_table_content = self.insert_linked_text(
                                        list_indexes=list_indexes
                                    )

        table_content = self.generate_table_content(list_indexes=list_indexes)
        # print("".join(res))
        if index_table_content is not None:
            left = self.data[:index_table_content + 2]
            content = self.contents_list
            right = self.data[index_table_content + 2:]
            self.data = left + content + right
        else:
            self.data = table_content + self.data

        if self.string is not None:
            print("".join(self.data))

        if self.filename is not None:
            self.to_write()

    def get_indexes(
        self
    ) -> list:
        """
        Gets all titles and their index from data of file.

        Returns
            list: list of tuples of indexs and text of titles.
        """
        indexes = []
        code_section = False
        for i in range(len(self.data)):
            if self.data[i].startswith('```'):
                code_section = not code_section

            if code_section is False:
                result = re.findall(
                                r'^\#{1,6}\s{1}(.)?[A-Za-z].*',
                                self.data[i],
                                re.DOTALL
                            )
                if result != []:
                    position_string = (i, self.data[i])
                    indexes.append(position_string)
        return indexes

    def insert_linked_text(
        self,
        list_indexes: list
    ) -> str:
        """
        Generates link of title.

        Parameters:
            line: str, title string Markdown.
        Returns:
            str: link of title.
        """
        keywords = ['content', 'contenido', 'índice', 'indice', 'index']
        index_table_content = None
        for line in list_indexes:
            title = line[1]
            link = self.__to_link(title)
            if link not in self.data:
                # print(link, title, title in self.data)
                # x = self.data.index(f'{title}\n')
                index = self.data.index(title)
                self.data.insert(index, f'{link}')
                self.data.insert(self.data.index(link) + 1, '\n')

                if index_table_content is None:
                    if title.replace("#", '').strip().lower() in keywords:
                        index_table_content = self.data.index(f'{title}\n')

        return index_table_content

    def __to_link(
        self,
        line: str
    ) -> str:
        """
        Generates link of title.

        Parameters:
            line: str, title string Markdown.
        Returns:
            str: link of title.
        """
        line = line.replace('#', '')
        line = line.strip().replace(' ', '-').lower()
        line = line.replace(':', '')
        line = line.replace('`', '')
        return f'<a name="{line}"></a>\n'

    def generate_table_content(
        self,
        list_indexes: list
    ) -> list:
        """
        Generates a table of contents of all the titles in the Markdown file.

        Args
            list_indexes: list of tuples of index of all titles from markdown \
            file.

        Returns
            list: list of strings with all titles formatted.
        """
        lvls = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1
        }
        result = []
        spaces = '    '

        for line in list_indexes:
            line = line[1]
            if line != "":
                level = line.count("#")

                title = line.replace("#", "").strip()
                link = title.replace(' ', '-').lower()
                link = link.replace(':', '')
                link = link.replace('`', '')

                link_title = f'[{title}](#{link})\n'

                lvl_string = f'{lvls[level]}. '.ljust(4)

                if level > 1:
                    if level == 2:
                        link_level = f'{spaces * (level - 1)}{lvl_string}'
                        lvls[level] += 1
                        lvls.update(
                            {i: 1 for i in list(lvls.keys())[2:]}
                        )

                    elif level == 3:
                        link_level = f'{spaces * (level - 1)}{lvl_string}'
                        lvls[level] += 1
                        if 'binario' in link_title:
                            print(link_title, level, level - 1)
                        lvls.update(
                            {i: 1 for i in list(lvls.keys())[3:]}
                        )
                    elif level == 4:
                        link_level = f'{spaces * (level - 1)}{lvl_string}'
                        lvls[level] += 1
                        lvls.update(
                            {i: 1 for i in list(lvls.keys())[4:]}
                        )
                    elif level == 5:
                        link_level = f'{spaces * (level - 1)}{lvl_string}'
                        lvls[level] += 1
                        lvls.update(
                            {i: 1 for i in list(lvls.keys())[5:]}
                        )
                    elif level == 6:
                        link_level = f'{spaces * (level - 1)}{lvl_string}'
                        lvls[level] += 1
                        lvls.update(
                            {i: 1 for i in list(lvls.keys())[6:]}
                        )

                elif level == 1:
                    link_level = lvl_string
                    lvls[1] += 1
                    lvls.update(
                        {i: 1 for i in list(lvls.keys())[1:]}
                    )

                link_title_complete = link_level + link_title

                result.append(link_title_complete)

        result += ['\n', '\pagebreak', '\n', '\n']

        return result

    def to_write(self) -> None:
        """
        Write the list of lines to a file ending with `_finish.md`.

        Returns:
            None
        """
        if self.filename is not None and self.string is None:
            filename = '%s%s%s' % (
                                self.name, LinkedText.PREFIX, self.extention
                            )
        if self.filename is None and self.string is not None:
            filename = 'linkedtext_finish.md'

        with open(filename, 'w') as filew:
            filew.writelines(self.data)
