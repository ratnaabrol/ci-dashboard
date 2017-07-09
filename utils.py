import json, time, os, queue
from datetime import datetime
from requests import HTTPError
from travis.client import Client
from threading import Thread
from github import Github
from tools import Tools

class Utils:
    def __init__(self):
        path = os.path.dirname(__file__)
        self.config_file = os.path.join(path, "config.json")
        self.config = self.readConfig()
        self.travis = Client(self.config['token'])
        self.tools = Tools()

    def readConfig(self):
        with open(self.config_file, 'r') as f:
            data = json.load(f)
        return data
    
    def saveConfig(self, **kwargs):
        for key, value in kwargs.items():
            self.config[key] = value  
        
        if 'token' in kwargs:
            self.travis.authorize(kwargs['token'])
            
        with open(self.config_file , 'w') as f:
            json.dump(self.config, f)

    def repo(self, slug):
        repo = self.travis.repo(slug).json()
        branches = self.branches(repo['id'])
        last_build = self.builds(repo['id'], last_build=True)
        if last_build:
            last_build = last_build[0]
            
        repo['branches'] = branches
        repo['last_build'] = last_build or None
        return repo

    def repos(self):
        try:
            member = self.travis.user().json()['login']
            repos = self.travis.repos(member=member, limit=1000, active=True).json()
            return repos['repositories']
        except HTTPError as e:
            return None

    def builds(self, repoid, last_build=False):
        if last_build:
            limit = 1
        else:
            limit = 10000
            
        builds = self.travis.builds(repoid, limit=limit)
        return builds.json()['builds']
 
    def branches(self, repoid):
        branches = self.travis.branches(repoid)
        return [branch['name'] for branch in branches.json()['branches']]
    
    def actions(self, **kwargs):
        action = kwargs['action']
    
        if action == 'trigger':
            repoid = kwargs['repoid']
            branch = kwargs['branch']
            data = {"request": {"branch": branch}}
            self.travis.trigger_build(repoid=repoid, data=data)

        elif action == 'restart':
            buildid = kwargs['buildid']
            self.travis.restart_build(buildid=buildid)

        elif action == 'cancel':
            buildid = kwargs['buildid']
            self.travis.cancel_build(buildid=buildid)
            
        else:
            raise RuntimeError('Invalid action')

    def getDashboard(self):
        dashboard_data = []
        repos = queue.Queue()

        for repo in self.config['repos']:
            repos.put(repo.replace('/', '%2F'))

        def collectData():
            while not repos.empty():
                slug = repos.get()
                repo = self.repo(slug)
                dashboard_data.append(repo)
        
        def workers():
            threads_list = []
            threads = self.config['threads']
            for i in range(threads):
                worker = Thread(target=collectData)
                threads_list.append(worker)
                worker.start()

            for thread in threads_list:
                thread.join()
            
            
            return sorted(dashboard_data, key=lambda k: k['slug'])
            
        return workers()

