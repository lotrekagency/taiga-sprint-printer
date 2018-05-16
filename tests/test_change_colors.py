import os
import shutil

from pathlib import Path

from taiga_sprint_printer.configuration import Configuration
from taiga_sprint_printer.change_colors import change_colors

from unittest.mock import Mock


class TestConfiguration:

    def _remove_config_folder(self):
        shutil.rmtree(self.config_folder)

    def _mock_prompts(self, mocker):
        self.mocked_ask_colors = mocker.patch('taiga_sprint_printer.change_colors.ask_colors')

    def _mock_expanduser(self, mocker):
        mocked_expanduser = mocker.patch('taiga_sprint_printer.configuration.os.path.expanduser')
        mocked_expanduser.return_value = self.home_folder

    def setup_method(self, test_method):
        self.home_folder = os.path.split(__file__)[0]
        self.config_folder = os.path.join(self.home_folder, '.config')

    def teardown_method(self, test_method):
        self._remove_config_folder()

    def test_change_colors(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)

        c = Configuration()

        assert c.get_config('colors', 'userstory') == 'red'
        assert c.get_config('colors', 'task') == 'blue'

        self.mocked_ask_colors.return_value = (
            'green',
            'red',
        )

        change_colors()

        assert c.get_config('colors', 'userstory') == 'green'
        assert c.get_config('colors', 'task') == 'red'
