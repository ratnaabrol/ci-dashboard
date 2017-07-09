from flask import Blueprint, Flask, request, redirect, render_template, url_for, stream_with_context
import argparse, json, time
from utils import Utils
from requests import HTTPError
from errors import errors
from flask import Response

app = Flask(__name__)

utils = Utils()

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard(): 
    if request.method == 'GET':
        config = utils.readConfig()
        repos = utils.getDashboard()
        return render_template("dashboard/dashboard.html", repos=repos, config=config, utils=utils)

    elif request.method == 'POST':
        if 'trigger' in request.form:
            repoid = request.form.get('repo')
            branch = request.form.get('branch')
            utils.actions(action='trigger', repoid=repoid, branch=branch)

        elif 'restart-build' in request.form:
            buildid = request.form.get('buildid')
            utils.actions(action='restart', buildid=buildid)
        
        elif 'cancel-build' in request.form:
            buildid = request.form.get('buildid')
            utils.actions(action='cancel', buildid=buildid)
        
        return redirect(url_for('dashboard'), code=302)


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    config = utils.config
    if request.method == 'GET':
        repos = utils.repos()
        return render_template('settings.html', repos=repos, config=config)
        
    elif request.method == 'POST':
        if 'configration' in request.form:
            token = request.form.get('token')
            github_token = request.form.get('github_token')
            threads = int(request.form.get('threads'))
            columns = int(request.form.get('columns'))
            interval = int(request.form.get('interval'))
            utils.saveConfig(token=token, 
                             github_token=github_token, 
                             threads=threads, 
                             columns=columns,
                             interval=interval)

        elif 'repositories' in request.form:
            repos = request.form.getlist("repos")
            utils.saveConfig(repos=repos)
            
        return redirect(url_for('settings'), code=302)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True, threaded=True)
