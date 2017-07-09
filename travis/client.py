import requests

class Client:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers = {
            'Accept':'MyClient/1.0.0',
            'User-Agent':'MyClient/1.0.0',
            'Content-Type':'application/json',
            'Travis-API-Version':'3',
            "Authorization":'token {}'.format(token)
        }
        self.base_url = 'https://api.travis-ci.org'
        
    def call_api(self, url, method='get', data=None, params=None):
        url = self.base_url + url
        if method == 'get':
            response = self.session.get(url, params=params)
        elif method == 'post':
            response = self.session.post(url, params=params, json=data)
        else:
            raise RuntimeError('Invalid request method')

        response.raise_for_status()
        return response

    def authorize(self, token):
        self.session.headers['Authorization'] = 'token {}'.format(token)

    def user(self):
        url = '/user'
        response = self.call_api(url)
        return response
        
    def repo(self, slug):
        url = '/repo/' + slug
        response = self.call_api(url)
        return response

    def repos(self, **params):
        url = '/repos'
        response = self.call_api(url, params=params)
        return response

    def branches(self, repoid, **params):
        url = '/repo/' + str(repoid) + '/branches'
        response = self.call_api(url, params=params)
        return response
    
    def builds(self, repoid, **params):
        url = '/repo/' + str(repoid) + '/builds'
        params['include'] = 'build.commit'
        response = self.call_api(url, params=params)
        return response

    def trigger_build(self, repoid, data):
        url = '/repo/' + str(repoid) + '/requests'
        response = self.call_api(url, method='post', data=data)
        return response

    def restart_build(self, buildid):
        url = '/build/' + str(buildid) + '/restart'
        response = self.call_api(url, method='post')
        return response

    def cancel_build(self, buildid):
        url = '/build/' + str(buildid) + '/cancel'
        response = self.call_api(url, method='post')
        return response
