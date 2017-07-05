from flask import Blueprint, Flask, request, redirect, render_template, url_for, stream_with_context
from travis_client.client import Client
import argparse, json, time
from utils import Utils
from requests import HTTPError
from errors import errors
from flask import Response

app = Flask(__name__)

@app.errorhandler(HTTPError)
def ApiErrorHandeler(e):
    status = e.response.status_code
    if status == 403:
        error = errors['001']
    else:
        error = errors['000']     
    return render_template('error.html', error=error, details=e.args[0])
    
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard(): 
    if request.method == 'GET':
        config = Utils().readConfig()
        repos = Utils().getDashboardData()
        return render_template("dashboard.html", repos=repos, config=config, utils=Utils())

    elif request.method == 'POST':
        if 'trigger' in request.form:
            repoid = request.form.get('repo')
            branch = request.form.get('branch')
            Utils().triggerBuild(repoid, branch)

        elif 'restart-build' in request.form:
            buildid = request.form.get('buildid')
            Utils().restartBuild(buildid)
        
        elif 'cancel-build' in request.form:
            buildid = request.form.get('buildid')
            Utils().cancelBuild(buildid)
        
        return redirect(url_for('dashboard'), code=302)

@app.route("/update")
def update():
    repos = Utils().getDashboardData()
    return json.dumps(repos)

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    config = Utils().readConfig()

    if request.method == 'GET':
        repos = Utils().getMyRepos()
        return render_template('settings.html', repos=repos, config=config)
        
    elif request.method == 'POST':
        if 'config-account' in request.form:
            config['token'] = request.form.get('token')
            config['github_token'] = request.form.get('github_token')

        elif 'config-dashboard' in request.form:
            selected_repos = request.form.getlist("repos")
            config['repos'] = selected_repos
            config['threads'] = int(request.form.get('threads'))
            config['interval'] = int(request.form.get('interval'))
            config['columns'] = int(request.form.get('columns'))
            
        Utils().saveConfig(config)
        return redirect(url_for('settings'), code=302)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True, threaded=True)
