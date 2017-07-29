from flask import Flask, request, redirect, render_template, url_for, Response, session, g
import argparse, json, requests, os, uuid
from lib.tools import Tools
from lib.dashboard import Dashboard
from lib.repositories import Repositories
from lib.clients.travis import Travis
from lib.authorizer import auth
from lib.http import HttpStatus


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

client_id = 'travis-dashboard'
client_secret = ''
redirect_url = 'http://127.0.0.1:5000/callback'

tools = Tools()
httpStatus = HttpStatus()
authorizer = auth(client_id, client_secret, redirect_url)

@app.context_processor
def user_auth_info():
    userInfo = authorizer.is_authorized_user()
    config = tools.read_config(protected=True)
    return dict(userInfo=userInfo, config=config)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard", methods=["POST"])
@authorizer.member_required
def build_actions():
    slug = request.form.get('repo')
    if 'trigger-build' in request.form:
        branch = request.form.get('branch')
        Repositories().repo(slug).trigger_build(branch)

    elif 'restart-build' in request.form:
        buildid = request.form.get('buildid')
        Repositories().repo(slug).restart_build(buildid)
    
    elif 'cancel-build' in request.form:
        buildid = request.form.get('buildid')
        Repositories().repo(slug).cancel_build(buildid)

    return redirect(url_for('dashboard'), code=302)


@app.route("/dashboard/fetch")
def fetch_dashboard(): 
    params = request.args.to_dict()
    headers, repos = Dashboard().fetch(** params)
    html = render_template("repos.html", repos=repos)
    return Response(html, headers=headers)

@app.route("/dashboard/modal")
@authorizer.member_required
def repo_modal():
    slug = request.args.get('slug')
    repo = Repositories().repo(slug)
    repo = {
        "info": repo.info(),  
        "branches":repo.branches(),
        "last_build": repo.last_build()
    }
    html = render_template("modal.html", repo=repo)
    return html

@app.route("/settings", methods=['GET', 'POST'])
@authorizer.member_required
def settings():
    success = None
    if request.method == 'POST':    
        if 'configration' in request.form:  
            travis_token = request.form.get('travis_token')
            github_token = request.form.get('github_token')
            threads = int(request.form.get('threads'))
            grid_size = int(request.form.get('grid_size'))
            interval = int(request.form.get('interval'))
            view_mode = request.form.get('view_mode')
            tools.save_config(threads=threads, 
                              grid_size=grid_size, 
                              interval=interval, 
                              travis_token=travis_token, 
                              github_token=github_token,
                              view_mode=view_mode)

        elif 'repositories' in request.form:
            selected_repos = request.form.getlist("repos")
            tools.save_config(repos=selected_repos)

        success = True

    repos = Repositories().list()
    return render_template('settings.html', repos=repos, success=success) 

@app.route("/login")
def itsyouonline_login():
    return render_template('login.html') 

@app.route("/auth")
def itsyouonline_auth():
    return authorizer.itsyouonline_auth()

@app.route("/callback")
def itsyouonline_callback():
    code = request.args.get('code') 
    state = request.args.get('state')
    if not code or state != authorizer.state:
        return httpStatus.BadRequest()

    authorizer.authorize_user(code, state)
    return redirect(url_for('dashboard'), code=302)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard"))

@app.route("/access_denied")
def access_denied():
    return render_template('access_denied.html')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    parser.add_argument("--clientid", type=str)
    parser.add_argument("--clientsecret", type=str)
    parser.add_argument("--org", type=str)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True, threaded=True)


