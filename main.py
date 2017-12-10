from flask import Flask, request, redirect, render_template, url_for, Response
import argparse, uuid
from lib.tools import Tools
from lib.dashboard import Dashboard
from lib.repositories import Repositories

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
tools = Tools()
repositories = Repositories(sticky_branch=None)

@app.context_processor
def context_processor():
    config = tools.read_config(protected=True)
    return dict(config=config)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard", methods=["POST"])
def build_actions():
    slug = request.form.get('repo')
    if 'trigger-build' in request.form:
        branch = request.form.get('branch')
        repositories.repo(slug).trigger_build(branch)

    elif 'restart-build' in request.form:
        buildid = request.form.get('buildid')
        repositories.repo(slug).restart_build(buildid)

    elif 'cancel-build' in request.form:
        buildid = request.form.get('buildid')
        repositories.repo(slug).cancel_build(buildid)

    return redirect(url_for('dashboard'), code=302)


@app.route("/dashboard/fetch")
def fetch_dashboard():
    params = request.args.to_dict()
    headers, repos = Dashboard().fetch(** params)
    html = render_template("repos.html", repos=repos)
    return Response(html, headers=headers)

@app.route("/dashboard/modal")
def repo_modal():
    slug = request.args.get('slug')
    repo = repositories.repo(slug)
    repo = {
        "info": repo.info(),
        "branches":repo.branches(),
        "last_build": repo.last_build(),
        "env_vars": repo.env_vars()
    }
    html = render_template("modal.html", repo=repo)
    return html

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    success = None
    if request.method == 'POST':
        if 'configration' in request.form:
            travis_for = request.form.get('travis_for')
            travis_token = request.form.get('travis_token')
            github_token = request.form.get('github_token')
            threads = int(request.form.get('threads'))
            grid_size = int(request.form.get('grid_size'))
            interval = int(request.form.get('interval'))
            view_mode = request.form.get('view_mode')
            sticky_branch = request.form.get('sticky_branch')
            tools.save_config(travis_for=travis_for,
                              threads=threads,
                              grid_size=grid_size,
                              interval=interval,
                              travis_token=travis_token,
                              github_token=github_token,
                              view_mode=view_mode,
                              sticky_branch=sticky_branch)

        elif 'repositories' in request.form:
            selected_repos = request.form.getlist("repos")
            tools.save_config(repos=selected_repos)

        success = True

    repos = repositories.list()
    return render_template('settings.html', repos=repos, success=success)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True, threaded=True)
