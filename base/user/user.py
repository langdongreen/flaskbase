from flask import render_template, url_for, request,Blueprint
from .user_utils import login_required

import logging

log = logging.getLogger(__name__)
user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/user')
@login_required
def user():
    '''Render index template with banner, cart and contact details.'''
    message = "user"

    return render_template('user.html',message = message)


def redirect_url(default='index'):
    return request.args.get('next') or \
       request.referrer or \
       url_for(default)  

