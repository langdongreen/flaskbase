from flask import render_template, url_for, request
from base import app
from .user_utils import login_required

@app.route('/user')
@login_required
def user():
    '''Render index template with banner, cart and contact details.'''
    message = "user"

    return render_template('user.html',message = message)


def redirect_url(default='index'):
    return request.args.get('next') or \
       request.referrer or \
       url_for(default)  

