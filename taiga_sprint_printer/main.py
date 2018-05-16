import argparse

from .change_colors import change_colors
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
        if args.command == 'colors':
            change_colors()
        else:
            print_sprint(args.command == 'new')
    except CancelledByUserError as ex:
        pass
