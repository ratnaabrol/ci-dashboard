# CI Dashboard
Travis CI builds dashboard written in python

![dashboard](/docs/dashboard.png)

### Installation
```bash
curl -sL https://raw.github.com/ahmedelsayed-93/ci-dashboard/master/scripts/install.sh | sudo bash 
```
### Getting started

- Start server
```bash
cidashboard start --host {{host}} --port {{port}}
```
> CI-Dashboard server will be started in a new tmux session named [cidashboard].
- Go to **Settings** page ```http:/{host}:{port}/settings```, and set your configrations.
- Go to **Dashboard** page ```http:/{host}:{port}/dashboard```, and have fun!. 

- For help 
```
cidashboard help 
```

### To do
- Error handling 

### Author
[Ahmed El-Sayed](mailto:ahmed.m.elsayed93@gmail.com)

