import logging

from flask import Flask,g,session

from base.login.login import login_blueprint
from base.user.user import user_blueprint
from base.public.public import public_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

#Blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(public_blueprint)

logging.basicConfig(filename='debug.log',level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s\
                    [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S')

#default template variables
@app.context_processor
def inject_variables():
    '''Set and return variables that are on every page'''
    
    if 'clientid' not in session:
        session['clientid'] = ''
        
    return { 'user': session['clientid']}

@app.before_request
def before_request():
    '''Check for logged in user and redirect if not logged in'''
    #add session to global variable
    if 'clientid' in session:
        g.user = session['clientid']
    else:
        g.user = ''


