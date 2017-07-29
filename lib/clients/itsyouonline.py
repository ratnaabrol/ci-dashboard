import requests, uuid

class Itsyouonline:
    def __init__(self, client_id, client_secret, callback_url):
        self.base_url = 'https://itsyou.online'
        self.session = requests.Session()
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.state = uuid.uuid4().hex[:5]
    
    def call_api(self, url, method='get', data=None, params=None):
        url = self.base_url + url
        if method == 'get':
            response = self.session.get(url, params=params)
        elif method == 'post':
            response = self.session.post(url, params=params, json=data)

        response.raise_for_status()
        return response


    def get_access_token(self, code, state):
        url = '/v1/oauth/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.callback_url,
            'state': state
        }
        response = self.call_api(url, method='post',params=params)
        return response