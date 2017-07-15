from flask import Flask, request, redirect, render_template, url_for, Response
import argparse, json, time
from utils import *
from tools import Tools
from requests import HTTPError
from repository import Repository

app = Flask(__name__)

tools = Tools()

@app.route("/")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    config = tools.read_config() 
    if request.method == 'GET':
        repos = get_dashboard()
        return render_template("dashboard.html", repos=repos, config=config)

    elif request.method == 'POST':
        if 'trigger' in request.form:
            repo = request.form.get('repo')
            branch = request.form.get('branch')
            Repository(repo).trigger_build(branch)

        elif 'restart-build' in request.form:
            repo = request.form.get('repo')
            buildid = request.form.get('buildid')
            Repository(repo).restart_build(buildid)
        
        elif 'cancel-build' in request.form:
            repo = request.form.get('repo')
            buildid = request.form.get('buildid')
            Repository(repo).cancel_build(buildid)

        return redirect(url_for('dashboard'), code=302)

@app.route("/dashboard/update")
def update_dashboard():
    repos = get_dashboard()
    html =  render_template("repo.html", repos=repos)
    return html

@app.route("/modal")
def repo_modal():
    slug = request.args.get('slug')
    repo = Repository(slug)
    repo = {"info": repo.info(), "last_build": repo.last_build(), "branches":repo.branches()}
    html =  render_template("modal.html", repo=repo)
    return html
    
@app.route("/settings", methods=['GET', 'POST'])
def settings():
    response = None
    config = tools.read_config()

    if request.method == 'POST':    
        if 'configration' in request.form:  
            travis_token = request.form.get('travis_token')
            github_token = request.form.get('github_token')
            threads = int(request.form.get('threads'))
            columns = int(request.form.get('columns'))
            interval = int(request.form.get('interval'))
            tools.save_config(travis_token=travis_token,
                              github_token=github_token,
                              threads=threads, 
                              columns=columns,
                              interval=interval)

        elif 'repositories' in request.form:
            selected_repos = request.form.getlist("repos")
            tools.save_config(repos=selected_repos)

        response = True
 
    return render_template('settings.html', 
                            repos=get_my_repos(), 
                            config=tools.read_config(), 
                            response=response)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True, threaded=True)
