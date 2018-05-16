import os
import shutil

from pathlib import Path

from taiga.models.base import SearchableList
from taiga.models import UserStory, Task

from taiga.exceptions import TaigaException

from taiga_sprint_printer.configuration import Configuration
from taiga_sprint_printer.print_sprint import print_sprint

from unittest.mock import Mock


class TestConfiguration:

    def _remove_config_folder(self):
        shutil.rmtree(self.config_folder)

    def _mock_prompts(self, mocker):
        self.mocked_ask_credentials = mocker.patch('taiga_sprint_printer.print_sprint.ask_credentials')
        self.mocked_ask_password = mocker.patch('taiga_sprint_printer.print_sprint.ask_password')
        self.mocked_ask_project = mocker.patch('taiga_sprint_printer.print_sprint.ask_project')
        self.mocked_ask_sprint = mocker.patch('taiga_sprint_printer.print_sprint.ask_sprint')
        self.mocked_ask_file_destination = mocker.patch('taiga_sprint_printer.print_sprint.ask_file_destination')

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

    def test_print_with_new_configuration(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)

        c = Configuration()
        c.set_config('taiga', 'host', 'https://notexistingtaiga.io/')
        c.set_config('taiga', 'user', 'astagi')

        self.mocked_ask_credentials.return_value = (
            'https://notexistingtaiga.io/',
            'astagi',
            '1t54s3cr3t'
        )

        assert print_sprint(True) == 1

        self.mocked_ask_credentials.assert_called()
        self.mocked_ask_password.assert_not_called()

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

    def test_print_sprint(self, mocker):
        self._mock_expanduser(mocker)
        self._mock_prompts(mocker)

        c = Configuration()
        c.set_config('taiga', 'host', 'https://notexistingtaiga.io/')
        c.set_config('taiga', 'user', 'astagi')

        self.mocked_ask_password.return_value = '1t54s3cr3t'
        taiga_api = mocker.patch('taiga_sprint_printer.print_sprint.TaigaAPI')

        self.mocked_ask_project.return_value = 'Project 1'
        self.mocked_ask_sprint.return_value = '1: Sprint 1'

        self.mocked_ask_file_destination.return_value = 'tests/generatedstuff/test.pdf'

        milestones = SearchableList()
        milestones.append(Mock())
        milestones.append(Mock())
        milestones[0].name = 'Sprint 1'
        milestones[0].id = 1
        milestones[1].name = 'Sprint 2'
        milestones[1].id = 2

        taiga_api.return_value.milestones.list.return_value = milestones

        stories = [
            UserStory(taiga_api, subject='Story 1'),
            UserStory(taiga_api, subject='Story 2')
        ]

        def mock_list_task():
            return [
                Task(None, subject='Task 1')
            ]

        stories[0].list_tasks = mock_list_task

        stories[1].list_tasks = mock_list_task

        taiga_api.return_value.user_stories.list.return_value = stories

        assert print_sprint() == 0

        taiga_api.return_value.user_stories.list.side_effect = TaigaException()

        assert print_sprint() == 1
