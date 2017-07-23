import requests

class Github:
    def __init__(self, github_token):
        self.base_url = 'https://api.github.com'
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token {}'.format(github_token)
        
    def call_api(self, url, method='get', data=None, params=None):
        url = self.base_url + url
        if method == 'get':
            response = self.session.get(url, params=params)
        elif method == 'post':
            response = self.session.post(url, params=params, json=data)

        response.raise_for_status()
        return response

    def branches(self, slug, **params):
        url = '/repos/' + slug + '/branches'
        response = self.call_api(url, params=params)
        return response
    
    