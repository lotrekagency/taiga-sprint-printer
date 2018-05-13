import os, shutil, configparser


class Configuration():

    def __init__(self):
        user_config_dir = os.path.join(
            os.path.expanduser("~"), '.config', 'sprint-printer'
        )
        self._user_config = os.path.join(
            user_config_dir, 'default.ini'
        )
        self._config = configparser.ConfigParser()

        if not os.path.isfile(self._user_config):
            os.makedirs(user_config_dir, exist_ok=True)

            self._config.add_section('colors')
            self._config['colors']['userstory'] = "red"
            self._config['colors']['task'] = "blue"

            with open(self._user_config, 'w') as f:
                self._config.write(f)

    def get_config(self):
        self._config.read(self._user_config)
        return self._config

    def set_section(self, section, value):
        pass