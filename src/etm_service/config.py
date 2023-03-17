'''
Singleton class containing the main config
'''

import yaml
from pathlib import Path

class Config:
    CONFIG_PATH = Path(__file__).parents[2].resolve() / 'config' / 'config.yml'
    FROM_CONF_PATH = True

    class __Config:
        def __init__(self, data):
            self.data = data

    instance = None
    def __init__(self):
        if not Config.instance:
            Config.instance = Config.__Config(self._load())

    def __getattr__(self, key):
        '''Get main keys of the config as attributes'''
        return self.instance.data.get(key, None)

    def __setattr__(self, key, value):
        self.instance.data[key] = value

    def _load(self):
        if not self.FROM_CONF_PATH:
            return {}

        with open(self.CONFIG_PATH, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return doc
