import json
from os import path
from datetime import datetime


class Tools:
    def __init__(self):
        config_path = path.dirname(path.dirname(path.abspath(__file__)))
        self.__config_file = path.join(config_path, "config.json")

    def read_config(self, protected=False):
        with open(self.__config_file, 'r') as f:
            config = json.load(f)

        if protected:
            travis_token = config['travis_token']
            github_token = config['github_token']
            config['travis_token'] = travis_token[:3] + (len(travis_token)-3) * '*'
            config['github_token'] = github_token[:3] + (len(github_token)-3) * '*'

        return config

    def save_config(self, **kwargs):
        config = self.read_config()
        for key, value in kwargs.items():
            if key in ['travis_token', 'github_token'] and '*' in value:
                continue
            config[key] = value

        with open(self.__config_file, 'w') as f:
            json.dump(config, f, indent=4, sort_keys=True)

    def convert_time_to_age(self, target):
        now = datetime.utcnow()
        target = datetime.strptime(target, '%Y-%m-%dT%H:%M:%SZ')
        age = now-target
        if age.days > 365:
            return '{} year ago'.format(int(age.days/360))
        elif age.days > 30:
            return '{} months ago'.format(int(age.days/30))
        elif age.days:
            return '{} days ago'.format(age.days)
        elif age.seconds > 3600:
            return '{} hours ago'.format(int(age.seconds/3600))
        elif age.seconds > 60:
            return '{} minutes ago'.format(int(age.seconds/60))
        elif age.seconds:
            return '{} seconds ago'.format(age.seconds)
