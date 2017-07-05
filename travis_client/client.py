import requests

class Client:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers = {
            'Accept':'MyClient/1.0.0',
            'User-Agent':'MyClient/1.0.0',
            'Content-Type':'application/json',
            'Travis-API-Version':'3',
            'Authorization':'token {}'.format(token)
        }

        self.base_url = 'https://api.travis-ci.org'
        
    def call_api(self, url, method='GET', data=None, params=None):
        url = self.base_url + url
        if method == 'GET':
            resp = self.session.get(url, params=params)
        elif method == 'POST':
            resp = self.session.post(url, params=params, json=data)
        resp.raise_for_status()
        return resp

    def user(self):
        url = '/user'
        resp = self.call_api(url)
        return resp.json()
        
    def repo(self, repo_slug):
        url = '/repo/' + repo_slug
        resp = self.call_api(url)
        return resp.json()

    def repos(self, member):
        url = '/repos'
        params = {'limit':10000, 'member':member, 'active':True, 'sort_by':'name'}
        resp = self.call_api(url, params=params)
        return resp.json()

    def branches(self, repoid):
        url = '/repo/' + str(repoid) + '/branches'
        params = {'limit':10000, 'exists_on_github':True}
        resp = self.call_api(url, params=params)
        return resp.json()
    
    def last_build(self, repoid):
        url = '/repo/' + str(repoid) + '/builds'
        params = {'limit':1, 'include':'build.commit'}
        resp = self.call_api(url, params=params)
        return resp.json()

    def trigger_build(self, repoid, data):
        url = '/repo/' + str(repoid) + '/requests'
        resp = self.call_api(url, method='POST', data=data)
        return resp.json()

    def restart_build(self, buildid):
        url = '/build/' + str(buildid) + '/restart'
        resp = self.call_api(url, method='POST')
        return resp.json()

    def cancel_build(self, buildid):
        url = '/build/' + str(buildid) + '/cancel'
        resp = self.call_api(url, method='POST')
        return resp.json()

    
    