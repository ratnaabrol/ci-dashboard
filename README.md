# CI Dashboard
Travis CI builds dashboard written in python

![dashboard](/docs/dashboard.png)

### Installation
```bash
curl -sL https://raw.github.com/ahmedelsayed-93/ci-dashboard/master/scripts/install.sh | sudo bash -s {{branch}} {{path}}
default branch: master , path: /opt
```
### Getting started

- start server
```bash
cidashboard start --host {{host}} --port {{port}}
```
> CI-Dashboard server will be started in a new tmux session named [cidashboard].
- Go to **Settings** page ```http:/{host}:{port}/settings```, and set your configrations.
- Go to **Dashboard** page ```http:/{host}:{port}/dashboard```, and have fun!. 

- for help 
```
cidashboard help 

CI-Dashboard help
    Options:
    start :        start the server.
        options:
        --host : the hostname to listen on, default 127.0.0.1
        --port : the port of the webserver, default 5000
    stop   :    stop the server.
    update :    update software.
```
### To do
- Error handling 

### Author
[Ahmed El-Sayed](mailto:ahmed.m.elsayed93@gmail.com)

