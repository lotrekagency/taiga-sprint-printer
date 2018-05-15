import configparser
import os


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

    def get_config(self, section=None, attribute=None):
        self._config.read(self._user_config)
        try:
            if section and not attribute:
                return self._config[section]
            elif section and attribute:
                return self._config[section][attribute]
            else:
                return self._config
        except KeyError:
            return None

    def set_config(self, section, attribute, value):
        self._config.read(self._user_config)
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config[section][attribute] = value

        with open(self._user_config, 'w') as f:
            self._config.write(f)
        return self._config
