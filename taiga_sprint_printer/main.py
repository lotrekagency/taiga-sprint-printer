from .errors import CancelledByUserError
from .print_sprint import print_sprint


def main():
    try:
        print_sprint()
    except CancelledByUserError as ex:
        pass
