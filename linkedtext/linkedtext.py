"""
Class to generate links and table of contents from a Markdown file, generating
a new final Markdown file with the links and table of contents generated.

The original file is never altered, the final or generated file ends with a
prefix `_finish.md`.
"""

from linkedtext.exceptions import FileNotFound
import re


class LinkedText:
    """
    Class that generates table of contents and links.
    """

    def __init__(
        self,
        filename: str = None
    ) -> None:
        """
        Constructor:

        Parameters:
            filename : str, name of file Markdown. Required.

        Return:
            None
        """
        self.filename = filename
        self.data = self.read(filename)
        self.indexes = []
        self.contents_list = ''

    def read(
        self,
        filename: str = None
    ) -> list:
        """
        Read data of file.

        Parameters:
            filename: str, Markdown file.

        Return:
            list: list of lines of file.

        Raise:
            FileNotFound: file not provided.
        """
        if filename is not None:
            with open(filename, 'r') as fl:
                return fl.readlines()
        else:
            raise FileNotFound('Need a file to start convert.')

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
        indexes = []
        code_section = False
        keywords = ['contenido', 'índice', 'indice', 'index']
        index_table_content = None

        for i in range(len(self.data)):
            r = re.findall(r'^\#{1,6} [A-Z].+', self.data[i])
            if '```' in self.data[i]:
                code_section = not code_section
            if r != []:
                if code_section is False:
                    indexes.append((i, r[0]))

        for line in indexes:
            title = line[1]
            link = self.__to_link(title)
            if link not in self.data:
                x = self.data.index(f'{title}\n')
                self.data.insert(x, f'{link}')
                self.data.insert(self.data.index(link) + 1, '\n')

                if index_table_content is None:
                    if title.replace("#", '').strip().lower() in keywords:
                        index_table_content = self.data.index(f'{title}\n')

        self.__to_index(indexes)

        if index_table_content is not None:
            left = self.data[:index_table_content + 2]
            content = self.contents_list
            right = self.data[index_table_content + 2:]
            self.data = left + content + right
        else:
            self.data = self.contents_list + self.data

        self.__to_write()

    def __to_index(
        self,
        list_indexes: list
    ) -> None:
        """
        Generates a table of contents of all the titles in the Markdown file.
        """
        lvls = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1
        }
        res = []

        for line in list_indexes:
            line = line[1]
            if line != "":
                level = line.count("#")
                title = line.replace("#", "").strip()
                link = title.replace(' ', '-').lower()
                link = link.replace(':', '')

                if level > 1:
                    r = f'{"    " * (level - 1)}{lvls[level]}. [{title}](#{link})\n'
                    lvls[level] += 1
                else:
                    r = f'{lvls[level]}. [{title}](#{link})\n'
                    lvls[1] += 1
                    lvls.update(
                        {i: 1 for i in list(lvls.keys())[1:]}
                    )
                res.append(r)
        [res.append(i) for i in ['\n', '\pagebreak', '\n', '\n']]

        self.contents_list = res

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
        return f'<a name="{line}"></a>\n'

    def __to_write(self) -> None:
        """
        Write the list of lines to a file ending with `_finish.md`.

        Returns:
            None
        """
        file = self.filename.split('.md')
        filename = f'{file[0]}_finish.md'

        with open(filename, 'w') as filew:
            filew.writelines(self.data)
