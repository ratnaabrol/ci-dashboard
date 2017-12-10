from lib.clients import Clients
from lib.repository import Repository

class Repositories(Clients):
    def __init__(self, sticky_branch):
        super().__init__()
        self.sticky_branch = sticky_branch

    def list(self):
        try:
            github_member = self._Clients__travis_client.user().json()['login']
            response = self._Clients__travis_client.repos(limit=100000, member=github_member, active=True)
            repos = [repo['slug'] for repo in response.json()['repositories']]
        except:
            repos = []
        return repos

    def repo(self, slug):
        return Repository(slug, self.sticky_branch)
