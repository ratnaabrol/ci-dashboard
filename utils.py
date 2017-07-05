import json, time, os, queue
from datetime import datetime
from requests import HTTPError
from travis_client.client import Client
from threading import Thread
from github import Github

class Utils:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.config = self.readConfig()
        self.repos = self.config['repos']
        self.token = self.config['token']
        self.github_token = self.config['github_token']
        self.threads = self.config['threads']
        self.client = Client(self.token)

    def readConfig(self):
        with open(self.config_file, 'r') as config_file:
            config_data = json.load(config_file)
        return config_data
    
    def saveConfig(self, config_data):
        with open(self.config_file , 'w') as config_file:
            json.dump(config_data, config_file)

    def getMyRepos(self):
        config = self.readConfig()
        try:
            github_member = self.client.user()['login']
            repos = self.client.repos(github_member)
        except HTTPError as e:
            return None

        return repos['repositories']
    
    def getBranches(self, repoid, reponame):
        if self.github_token:
            github_client = Github(login_or_token=self.github_token).get_user()
            repo = github_client.get_repo(reponame)
            branches = [branch.name for branch in repo.get_branches()]
            return branches
        else:
            branches = self.client.branches(repoid)
            return [branch['name'] for branch in branches['branches']]
        
    def getLastBuild(self, repoid):
        last_build = self.client.last_build(repoid)
        return last_build['builds']

    def triggerBuild(self, repoid, branch):
        data = {"request": {"branch": branch}}
        self.client.trigger_build(repoid, data)

    def restartBuild(self, buildid):
        self.client.restart_build(buildid)

    def cancelBuild(self, buildid):
        self.client.cancel_build(buildid)

    def getDashboardData(self):
        config = self.readConfig()
        selected_repos = queue.Queue()
        dashboard_data = []

        for repo in self.repos:
            selected_repos.put(repo)

        def collectData():
            while not selected_repos.empty():
                repo_slug = selected_repos.get().replace('/', '%2F')
                repo = self.client.repo(repo_slug)
                data = {
                    "repo_id" : repo['id'],
                    "repo_name" : repo['name'],
                    "repo_slug" : repo['slug'],
                    "default_branch" : repo['default_branch']['name'],
                    "last_build" : None,
                    "branches" : self.getBranches(repo['id'], repo['name'])
                }

                last_build = self.getLastBuild(repo['id'])
                if last_build:
                    last_build = last_build[0]
                    data['last_build'] = {
                        "id" : last_build['id'],
                        "number" : last_build['number'],
                        "duration": last_build['duration'],
                        "state" : last_build['state'].upper(),
                        "previous_state" : last_build['previous_state'],
                        "event_type": last_build['event_type'].replace('_', ' ').title(),
                        "started_at" : last_build['started_at'],
                        "finished_at" : last_build['finished_at'],
                        "pull_request_title" : last_build['pull_request_title'],
                        "pull_request_number" : last_build['pull_request_number'],
                        "branch" : last_build['branch']['name'],
                        "commit_id": last_build['commit']['sha'][:7],
                        "commit_url": last_build['commit']['compare_url'],
                        "commit_message" : last_build['commit']['message'],
                        "commit_author": last_build['commit']['author']['name']
                    }
   
                dashboard_data.append(data)
        
        def workers():
            threads_list = []
            for i in range(self.threads):
                worker = Thread(target=collectData)
                threads_list.append(worker)
                worker.start()
            for thread in threads_list:
                thread.join()
            return dashboard_data
        return workers()


    def getItemAge(self, target):
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
        
    def splitList(self, item, n):
        return [item[i:i+n] for i in range(0, len(item), n)]
