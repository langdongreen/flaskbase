from flask import Flask,g,session
import logging
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from base.tools import jsonconfig as config

app = Flask(__name__)
app.config.from_pyfile('../config.py')
logging.basicConfig(filename='debug.log',level=logging.DEBUG, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S')

mail = Mail(app)
app.config['WTF_CSRF_SECRET_KEY'] = app.config["SECRET_KEY"]

#key for email verification
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
c = config.get_config()

#default template variables
@app.context_processor
def inject_variables():
    '''Set and return variables that are on every page'''
    
    if 'clientid' not in session:
        session['clientid'] = ''
        
    return {'title': c['name'],
            'banner': c['banner'],
            'user': session['clientid']}

@app.before_request
def before_request():
    '''Check for logged in user and redirect if not logged in'''
    #add session to global variable
    if 'clientid' in session:
        g.user = session['clientid']
        if g.user in c['admin']:
            g.admin = True
    else:
        g.user = ''

'''
    #restrict client pages
    if request.path.startswith('/client/'):
        if not g.user:
            return redirect(url_for('client_login'))

    #restrict admin pages
    if request.path.startswith('/admin'):

        if not g.user:
            return redirect(url_for('client_login'))
        elif not g.user in c['admin']:
            return redirect(url_for('client_dashboard'))
'''

'''@app.after_request
def add_header(response):
    response.cache_control.no_cache = 1
    response.cache_control.max_age = 0
    return response'''

'''Import application files'''
from base.user import user
from base.login import login
from base.public import public


