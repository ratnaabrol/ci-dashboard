import requests

class Github:
    def __init__(self, github_token):
        self.base_url_template = 'https://{}github.com'
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token {}'.format(github_token)
        self.api_url = self.base_url_template.format("api.")
        self.repo_url_template = "{}/{{slug}}".format(self.base_url_template.format(""))

    def call_api(self, url, method='get', data=None, params=None):
        url = self.api_url + url
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

    def get_repo_url(self, slug):
        return self.repo_url_template.format(slug=slug)
