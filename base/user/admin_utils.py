import logging
from flask import g,redirect,url_for,request
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user is '':
            return redirect(url_for('client_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
