from flask import Flask, request, redirect, render_template, url_for, Response
import argparse, json
from lib.tools import Tools
from lib.dashboard import Dashboard
from lib.repositories import Repositories
from lib.clients.travis import Travis

app = Flask(__name__)
tools = Tools()

@app.route("/")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == 'GET':
        return render_template("dashboard.html", config=tools.read_config())

    elif request.method == 'POST':
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
def fetch_dashboard_page(): 
    page = int(request.args.get('page')) 
    event_type = request.args.get('event_type')  
    number_of_pages, last_page, repos = Dashboard().fetch_page(page=page, event_type=event_type)
    html = render_template("repos.html", repos=repos)
    return Response(html, headers={'last_page':last_page, 'pages':number_of_pages}) 

@app.route("/dashboard/modal")
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
def settings():
    success = None
    if request.method == 'POST':    
        if 'configration' in request.form:  
            travis_token = request.form.get('travis_token')
            github_token = request.form.get('github_token')
            threads = int(request.form.get('threads'))
            grid_size = int(request.form.get('grid_size'))
            interval = int(request.form.get('interval'))
            tools.save_config(threads=threads, 
                              grid_size=grid_size, 
                              interval=interval, 
                              travis_token=travis_token, 
                              github_token=github_token)

        elif 'repositories' in request.form:
            selected_repos = request.form.getlist("repos")
            tools.save_config(repos=selected_repos)

        success = True

    repos = Repositories().list()
    config = tools.read_config(protected=True)
    return render_template('settings.html', repos=repos, config=config, success=success) 
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default='127.0.0.1', help="the hostname to listen on")
    parser.add_argument("--port", type=int, default=5000, help="the port of the webserver")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True, threaded=True)
