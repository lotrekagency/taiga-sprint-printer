
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colored_message(color, message):
    return '{0}{1}{2}'.format(color, message, BColors.ENDC)


def success_message(message):
    return '{0} {1}'.format(
        colored_message(BColors.OKGREEN, 'success'), message
    )


def warning_message(message):
    return '{0} {1}'.format(
        colored_message(BColors.WARNING, 'warning'), message
    )


def error_message(message):
    return '{0} {1}'.format(
        colored_message(BColors.FAIL, 'error'), message
    )


def progress_message(complete, total, message):
    return '[{0}/{1}] {2}'.format(complete, total, message)
