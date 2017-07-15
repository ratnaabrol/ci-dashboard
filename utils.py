import json, time, os, queue
from threading import Thread
from tools import Tools
from repository import Repository
from travis.client import Client

tools = Tools()
travis = Client(tools.read_config()['travis_token'])

def get_my_repos():
    token = tools.read_config()['travis_token']
    travis = Client(token)
    try:
        github_member = travis.user().json()['login']
        repos = travis.repos(limit=100000, member=github_member, active=True).json()['repositories'] 
    except:
        repos = []

    return  repos

def get_dashboard():
    
    dashboard = []
    config = tools.read_config()
    repos = queue.Queue()

    for repo in config['repos']:
        repos.put(repo)

    def collectData():
        while not repos.empty():
            slug = repos.get()
            repo = Repository(slug)
            data = {
                "info": repo.info(),
                "last_build": repo.last_build()
            }
            dashboard.append(data)
    
    def workers():
        threads_list = []
        threads = config['threads']
        for i in range(threads):
            worker = Thread(target=collectData)
            threads_list.append(worker)
            worker.start()

        for thread in threads_list:
            thread.join()
        
        return sorted(dashboard, key=lambda k: k['info']['slug'])

    return workers()
    
