import os
import shutil

from taiga.exceptions import TaigaException

from taiga_sprint_printer.configuration import Configuration
from taiga_sprint_printer.print_sprint import print_sprint


class TestConfiguration:

    def _remove_config_folder(self):
        shutil.rmtree(self.config_folder)

    def _mock_prompts(self, mocker):
        self.mocked_ask_credentials = mocker.patch('taiga_sprint_printer.print_sprint.ask_credentials')
        self.mocked_ask_password = mocker.patch('taiga_sprint_printer.print_sprint.ask_password')
        self.mocked_ask_project = mocker.patch('taiga_sprint_printer.print_sprint.ask_project')
        self.mocked_ask_sprint = mocker.patch('taiga_sprint_printer.print_sprint.ask_sprint')

    def _mock_expanduser(self, mocker):
        mocked_expanduser = mocker.patch('taiga_sprint_printer.configuration.os.path.expanduser')
        mocked_expanduser.return_value = self.home_folder

    def setup_method(self, test_method):
        self.home_folder = os.path.split(__file__)[0]
        self.config_folder = os.path.join(self.home_folder, '.config')

    def teardown_method(self, test_method):
        self._remove_config_folder()

    def test_print_with_no_configuration(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)
        self.mocked_ask_credentials.return_value = (
            'https://notexistingtaiga.io/',
            'astagi',
            '1t54s3cr3t'
        )
        assert print_sprint() == 1
        self.mocked_ask_credentials.assert_called()
        self.mocked_ask_password.assert_not_called()

    def test_print_with_configuration(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)

        c = Configuration()
        c.set_config('taiga', 'host', 'https://notexistingtaiga.io/')
        c.set_config('taiga', 'user', 'astagi')

        self.mocked_ask_password.return_value = '1t54s3cr3t'

        assert print_sprint() == 1
        
        self.mocked_ask_credentials.assert_not_called()
        self.mocked_ask_password.assert_called()


    def test_set_configuration_on_taiga_success(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)
        taiga_api = mocker.patch('taiga_sprint_printer.print_sprint.TaigaAPI')
        self.mocked_ask_credentials.return_value = (
            'https://newhosttaiga.io/',
            'astagiuser',
            '1t54s3cr3t'
        )

        taiga_api.return_value.projects.get_by_slug.side_effect = TaigaException()
        assert print_sprint() == 1
        c = Configuration()
        assert c.get_config('taiga', 'host') == 'https://newhosttaiga.io/'
        assert c.get_config('taiga', 'user') == 'astagiuser'
