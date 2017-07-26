from lib.tools import Tools
from lib.clients.travis import Travis
from lib.clients.github import Github

class Clients:
    def __init__(self):
        self.__tools = Tools()
        self.__config = self.__tools.read_config()
        self.__travis_token = self.__config['travis_token']
        self.__github_token = self.__config['github_token']
        self.__travis_client = Travis(self.__travis_token)
        self.__github_client = Github(self.__github_token)