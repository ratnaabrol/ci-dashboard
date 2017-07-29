# CI Dashboard
Travis CI builds dashboard written in python

![dashboard](/docs/dashboard.png)

### Installation
```bash
curl -sL https://raw.github.com/ahmedelsayed-93/ci-dashboard/itsyouonline-auth/scripts/install.sh | sudo bash 
```
### Getting started

#### Itsyou.online
- Create account on [itsyou.online](http://itsyou.online)
- Create a new organization.
- From you organization settings page create API key.
- Set the callback url to {{http or https}}://{{host}}:{{port}}/callback, for example:
    - ```https://travis-dash.gig.tech/callback```

#### Start server
```bash
cidashboard start [arguments]
Arguments
    --host          :   the hostname to listen on, default 127.0.0.1
    --port          :   the port of the webserver, default 5000
    --clientid      :   itsyouonline organization global id 
    --clientsecret  :   itsyouonline organization client secret
    --callbackurl   :   callback url {{http or https}}://{{host}}:{{port}}/callback
```

> CI-Dashboard server will be started in a new tmux session named [cidashboard].

#### Set your configration

- Go to **Settings** page ```http://{host}:{port}/settings```, and set the following parameters :

    - ```Travis token```: your travis token. [need help?](https://docs.travis-ci.com/api/#authentication)

    - ```Github token```: your github account token. [need help?](https://github.com/settings/tokens)
        > Optional. you will need it in case you want to trigger new builds from the dashboard.

    - ```Interval ```  : update interval in millisecond.

    - ```Grid size```  : number of columns and rows to be shown in the dashboard.
    
    - ```View mode```  : **onepage** or **slideshow**.

    - ```Threads```    : number of threads to fetch repositories info in the same time.


#### Open dashboard 
 - Go to **Dashboard** page ```http:/{host}:{port}/dashboard```, and have fun!. 

#### Help 
```
cidashboard help 
```

### To do
- Error handling 

### Thanks
- To [John Kheir](https://github.com/john-kheir) for his valuable remarks

### Author
[Ahmed El-Sayed](mailto:ahmed.m.elsayed93@gmail.com)

