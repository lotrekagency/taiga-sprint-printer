import os
import shutil

from taiga_sprint_printer.configuration import Configuration


class TestConfiguration:

    def _remove_config_folder(self):
        shutil.rmtree(self.config_folder)

    def _mock_expanduser(self, mocker):
        mocked_expanduser = mocker.patch('taiga_sprint_printer.configuration.os.path.expanduser')
        mocked_expanduser.return_value = self.home_folder

    def setup_method(self, test_method):
        self.home_folder = os.path.split(__file__)[0]
        self.config_folder = os.path.join(self.home_folder, '.config')

    def teardown_method(self, test_method):
        self._remove_config_folder()

    def test_configuration(self, mocker):
        self._mock_expanduser(mocker)
        c = Configuration()
        assert c.get_config()['colors'] == {
            'task' : 'blue',
            'userstory' : 'red'
        }
        assert c.get_config('colors') == {
            'task' : 'blue',
            'userstory' : 'red'
        }
        assert c.get_config('colors', 'task') == 'blue'
        assert c.get_config('colors', 'userstory') == 'red'

    def test_not_existing_value_in_configuration(self, mocker):
        self._mock_expanduser(mocker)
        c = Configuration()
        assert c.get_config('colors', 'issue') == None

    def test_set_configuration(self, mocker):
        self._mock_expanduser(mocker)
        c = Configuration()
        c.set_config('colors', 'issue', 'green')
        assert c.get_config('colors', 'issue') == 'green'
        c.set_config('colors', 'issue', 'pink')
        assert c.get_config('colors', 'issue') == 'pink'
        c.set_config('host', 'url', 'https://taiga.io/')
        assert c.get_config('host', 'url') == 'https://taiga.io/'