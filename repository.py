from clients.travis import Travis
from clients.github import Github
from tools import Tools
from requests import HTTPError

class Repository:
    def __init__(self, slug):
        self.slug = slug.replace('/', '%2F')
        self.travis_url = "https://travis-ci.org/{slug}".format(slug=slug)
        self.github_url = "http://github.com/{slug}".format(slug=slug)
        self.__tools = Tools()
        self.__config = self.__tools.read_config()
        self.__travis_client = Travis(self.__config['travis_token'])
        self.__github_token = self.__config['github_token']
        if self.__github_token:
            self.__github_client = Github(self.__github_token)
    
    def info(self):
        repo = self.__travis_client.repo(self.slug).json()
        return self.__repoParser(repo)

    def last_build(self):
        builds = self.__travis_client.builds(self.slug, limit=1).json()['builds']
        if builds:
            last_build = builds[0]
            return self.__buildParser(last_build)
        else:
            return None
        
    def branches(self):
        if self.__github_token:
            response = self.__github_client.branches(self.slug.replace('%2F', '/'))
            if response.status_code == 200:
                branches = [branch['name'] for branch in response.json()]
        else:
            branches = self.__travis_client.branches(self.slug, exists_on_github='true').json()
            branches = [branch['name'] for branch in branches['branches']]
        return branches
    
    def trigger_build(self, branch):
        data = {"request": {"branch": branch}}
        self.__travis_client.trigger_build(self.slug, data)
    
    def restart_build(self, buildid):
        self.__travis_client.restart_build(buildid)
    
    def cancel_build(self, buildid):
        self.__travis_client.cancel_build(buildid)

    def __repoParser(self, repo):
        data = {
            "id": repo['id'],
            "name": repo['name'],
            "slug": repo['slug'],
            "owner": repo['owner']['login'],
            "url": self.travis_url,
            "default_branch": repo['default_branch']['name']
        }
        return data


    def __buildParser(self, build):
        commit_url = self.github_url + "/commit/{sha}"
        build_url = self.travis_url + "/builds/{id}"

        data = {
            "id": build['id'],
            "number": build['number'],
            "state": build['state'].upper(),
            "url": build_url.format(id=build['id']),
            "branch": build['branch']['name'],
            "commit_sha": build['commit']['sha'][:7],
            "commit_author": build['commit']['author']['name'],
            "commit_url": commit_url.format(sha=build['commit']['sha'])
        }

        if build['event_type'] == 'pull_request':
            data['event'] = 'Pull Request #{}'.format(build['pull_request_number'])
            data['event_title'] = build['pull_request_title']
        else:
            data['event'] = build['event_type'].title()
            data['event_title'] = build['commit']['message']

        if build['state'] == 'started':
            time_event = 'Running for {}'.format(self.__tools.convert_time_to_age(build['started_at']))
            data['time_event'] = time_event

        elif build['state'] != 'created':
            time_event = 'Finished {}'.format(self.__tools.convert_time_to_age(build['finished_at']))
            data['time_event'] = time_event
            
        return data