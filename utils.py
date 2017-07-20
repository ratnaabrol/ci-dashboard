import json, time, os, queue
from threading import Thread
from tools import Tools
from repository import Repository
from clients.travis import Travis

tools = Tools()
travis = Travis(tools.read_config()['travis_token'])

def get_my_repos():
    token = tools.read_config()['travis_token']
    travis = Travis(token)
    try:
        github_member = travis.user().json()['login']
        repos = travis.repos(limit=100000, member=github_member, active=True).json()['repositories'] 
    except:
        repos = []

    return repos

def get_dashboard(event_type=None):
    
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
                "last_build": repo.last_build(event_type=event_type)
            }

            if data['last_build'] or event_type == 'all':
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
    
