import os

from taiga_sprint_printer.utils import get_current_dir


def test_current_directory():
    assert get_current_dir().endswith('/taiga_sprint_printer')
