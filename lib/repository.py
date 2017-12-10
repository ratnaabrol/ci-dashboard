from lib.clients import Clients


class Repository(Clients):
    def __init__(self, slug, sticky_branch):
        super().__init__()
        self.slug = slug
        self.sticky_branch = sticky_branch
        self.slug_encoded = slug.replace('/', '%2F')
        self.travis_url = self._Clients__travis_client.get_repo_url(slug)
        self.github_url = self._Clients__github_client.get_repo_url(slug)

    def info(self):
        info = {
            "slug" : self.slug,
            "owner" : self.slug.split('/')[0],
            "name" : self.slug.split('/')[1],
            "url" : self.travis_url
        }
        return info

    def _last_build_on_default_branch(self, **params):
        params['include'] = 'repository.default_branch,branch.last_build,build.commit'
        repo = self._Clients__travis_client.repo(self.slug_encoded, **params).json()
        default_branch = repo['default_branch']
        last_build = default_branch['last_build']
        if last_build:
            return self.__buildParser(last_build)
        return []

    def _last_build_on_sticky_branch(self, **params):
        builds = self._Clients__travis_client.builds(self.slug_encoded, **params).json()['builds']
        build = [b for b in builds if b["branch"]["name"] == self.sticky_branch]
        if len(build) > 0:
            return self.__buildParser(build[0])
        return[]

    def last_build(self, default_branch=False, **params):
        if default_branch:
            return self._last_build_on_default_branch(**params)

        if self.sticky_branch and len(self.sticky_branch):
            return self._last_build_on_sticky_branch(**params)

        params['limit'] = 1
        builds = self._Clients__travis_client.builds(self.slug_encoded, **params).json()['builds']
        if not builds:
            return []
        return self.__buildParser(builds[0])

    def branches(self):
        try:
            response = self._Clients__github_client.branches(self.slug)
            branches = [branch['name'] for branch in response.json()]
        except:
            branches = []
        return branches

    def env_vars(self):
        env_vars = self._Clients__travis_client.env_vars(self.slug_encoded).json()['env_vars']
        return env_vars

    def trigger_build(self, branch):
        data = {"request": {"branch": branch}}
        self._Clients__travis_client.trigger_build(self.slug_encoded, data)

    def restart_build(self, buildid):
        self._Clients__travis_client.restart_build(buildid)

    def cancel_build(self, buildid):
        self._Clients__travis_client.cancel_build(buildid)

    def __buildParser(self, build):
        commit_url = self.github_url + "/commit/{sha}"
        build_url = self.travis_url + "/builds/{id}"
        last_build = {
            "id": build['id'],
            "number": build['number'],
            "state": build['state'].upper(),
            "url": build_url.format(id=build['id']),
            "branch": build['branch']['@href'].split('/')[-1],
            "commit_sha": build['commit']['sha'][:7],
            "commit_author": build['commit']['author']['name'],
            "commit_url": commit_url.format(sha=build['commit']['sha'])
        }

        if build['event_type'] == 'pull_request':
            last_build['event'] = 'Pull Request #{}'.format(build['pull_request_number'])
            last_build['event_title'] = build['pull_request_title']
        else:
            last_build['event'] = build['event_type'].title()
            last_build['event_title'] = build['commit']['message']

        if build['state'] == 'started':
            time_event = self._Clients__tools.convert_time_to_age(build['started_at'])
            time_event = 'Running for {}'.format(time_event)
            last_build['time_event'] = time_event

        elif build['state'] != 'created':
            time_event = self._Clients__tools.convert_time_to_age(build['finished_at'])
            time_event = 'Finished {}'.format(time_event)
            last_build['time_event'] = time_event

        return last_build
