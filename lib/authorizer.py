import uuid, urllib
from functools import wraps
from datetime import datetime, timedelta
from flask import request, redirect, session, url_for
from lib.clients.itsyouonline import Itsyouonline
from lib.http import HttpStatus

httpStatus = HttpStatus()

class auth:
    def __init__(self, client_id, client_secret, redirect_url):
        self.client_id = client_id
        self.organization = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.state = uuid.uuid4().hex[:5]
        self.required_scope = 'user:name,user:memberof:{}'.format(self.organization)
        self.auth_url = 'https://itsyou.online/v1/oauth/authorize?'

    def itsyouonline_auth(self):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'scope': self.required_scope,
            'state': self.state
        }
        params = urllib.parse.urlencode(params)
        return redirect(self.auth_url + params)


    def authorize_user(self, code, state):            
        iyo_client = Itsyouonline(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  redirect_url=self.redirect_url)

        payload = iyo_client.get_access_token(code, state).json()
        session['username'] = payload['info']['username']
        session['access_token'] = payload['access_token']
        session['member'] = payload['scope'] == self.required_scope

    
    def is_authorized_user(self):
        if not self.__is_valid_session():
            return False

        info = {
            'username': session['username'],
            'member': session['member']
        }
        return info

    def __is_valid_session(self):
        if not session:
            return False

        required_keys = ['username', 'access_token', 'member']
        return all([x in session for x in required_keys])


    def member_required(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.__is_valid_session():
                return redirect('/login', code=302)    

            if not session['member']:
                return redirect('access_denied', code=302)
                
            return func(*args, **kwargs)            
        return decorator


    

        
    

        
    

        
    