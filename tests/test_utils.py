import os

from taiga_sprint_printer.utils import get_current_dir


def test_current_directory():
    assert 'print_taiga_sprint/taiga_sprint_printer' in get_current_dir()