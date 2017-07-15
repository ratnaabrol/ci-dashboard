import requests

class Github:
    def __init__(self, token=None):
        self.base_url = 'https://api.github.com'
        self.session = requests.Session()
        if token:
            self.session.headers['Authorization'] = 'token {}'.format(token)
        
    def call_api(self, url, method='get', data=None, params=None):
        url = self.base_url + url
        if method == 'get':
            response = self.session.get(url, params=params)
        elif method == 'post':
            response = self.session.post(url, params=params, json=data)
        else:
            raise RuntimeError('Invalid request method')
        return response

    def branches(self, slug, **params):
        url = '/repos/' + slug + '/branches'
        response = self.call_api(url, params=params)
        return response
    
    