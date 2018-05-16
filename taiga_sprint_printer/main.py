import argparse

from .errors import CancelledByUserError
from .print_sprint import print_sprint


def main():
    parser = argparse.ArgumentParser(
        description='Taiga Sprint Printer - Print your sprints on paper'
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=['new', 'colors'],
        help='new, colors (default: %(default)s)'
    )
    args = parser.parse_args()
    try:
        print_sprint(args.command == 'new')
    except CancelledByUserError as ex:
        pass
