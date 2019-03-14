import logging
from flask import g,redirect,url_for,request
from functools import wraps

log = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user is '':
            return redirect(url_for('login.client_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function