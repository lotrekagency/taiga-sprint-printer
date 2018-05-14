from taiga_sprint_printer.messages import BColors, colored_message, success_message
from taiga_sprint_printer.messages import warning_message, error_message, progress_message


def test_colored_message():
    assert colored_message(BColors.OKBLUE, 'hello!') == '\x1b[94mhello!\x1b[0m'


def test_success_message():
    assert success_message('Everything\'s fine!') == '\x1b[92msuccess\x1b[0m Everything\'s fine!'


def test_warning_message():
    assert warning_message('Warning!') == '\x1b[93mwarning\x1b[0m Warning!'


def test_error_message():
    assert error_message('There\'s an error!') == '\x1b[91merror\x1b[0m There\'s an error!'


def test_progress_message():
    assert progress_message(1, 5, 'First step') == '[1/5] First step'
    assert progress_message(2, 5, 'Second step') == '[2/5] Second step'