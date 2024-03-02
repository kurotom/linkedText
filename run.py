# -*- coding: utf-8 -*-
"""
Sample run.
"""


from linkedtext import LinkedText
import sys
import os



def run(
    file: str = None,
    string: str = None
):
    linked = LinkedText(
                    markdown_file=file,
                    string=string
                )
    linked.process()

data = sys.argv[1]

if os.path.isfile(data) or os.path.isdir(data):
    run(file=data)
elif isinstance(data, str):
    run(string=data)
