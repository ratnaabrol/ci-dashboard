# CI Dashboard
Travis CI builds dashboard written in python

![dashboard](/docs/dashboard.png)

### Installation

#### Quick start
```bash
git clone https://github.com/ahmedelsayed-93/ci-dashboard
cd ci-dashboard
python3 main.py --host ${host} --port ${port} 
```
#### Full installation
```bash
sudo curl -sL https://raw.github.com/ahmedelsayed-93/ci-dashboard/master/scripts/install.sh | bash -s {{branch}} {{path}}
default branch: master , path: /opt
```
### How to use
```bash
CI-Dashboard help
    Options:
    start :        start the server.
        options:
        --host : the hostname to listen on, default 127.0.0.1
        --port : the port of the webserver, default 5000
    stop   :    stop the server.
    update :    update software.
```

#### Start
```bash
cidashboard start --host {{host}} --port {{port}}
```

CI-Dashboard server will be started in new tmux session named [cidashboard].
- Go to settings page **(http:/{host}:{port}/settings)**, and set your configrations.
- Go to Dashboard page **(http:/{host}:{port}/dashboard)**, and have fun!.

### To do
- Error handling 

### Author
[Ahmed El-Sayed](mailto:ahmed.m.elsayed93@gmail.com)

