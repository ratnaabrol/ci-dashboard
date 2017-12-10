import requests


class Travis:
    def __init__(self, travis_token, travis_for="open-source"):
        self.session = requests.Session()
        self.session.headers = {
            'Accept':'application/vnd.travis-ci.2+json',
            'User-Agent':'MyClient/1.0.0',
            'Content-Type':'application/json',
            'Travis-API-Version':'3',
            'Authorization':'token {}'.format(travis_token)
        }
        self.base_url_template = 'https://{}travis-ci.org'
        if travis_for == "private-projects":
            self.base_url_template = "https://{}travis-ci.com"
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

    def user(self):
        url = '/user'
        response = self.call_api(url)
        return response

    def repo(self, slug, **params):
        url = '/repo/' + slug
        response = self.call_api(url, params=params)
        return response

    def repos(self, **params):
        url = '/repos'
        response = self.call_api(url, params=params)
        return response

    def branches(self, slug, **params):
        url = '/repo/' + slug + '/branches'
        response = self.call_api(url, params=params)
        return response

    def env_vars(self, slug, **params):
        url = '/repo/' + slug + '/env_vars'
        response = self.call_api(url, params=params)
        return response

    def builds(self, slug, **params):
        url = '/repo/' + slug + '/builds'
        params['include'] = 'build.commit'
        response = self.call_api(url, params=params)
        return response

    def trigger_build(self, slug, data):
        url = '/repo/' + slug + '/requests'
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

    def get_repo_url(self, slug):
        return self.repo_url_template.format(slug=slug)
