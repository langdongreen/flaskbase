'''Perform user creation and login functions for application'''
import logging

from itsdangerous import URLSafeTimedSerializer
from flask import (render_template,
                   request,
                   flash,
                   session,
                   url_for,
                   redirect,
                   g,
                   Blueprint)
from flask import current_app as app


from .login_form import LoginForm
from .login_utils import (user_exists,
                          login_user,
                          new_user,
                          confirm_user,
                          user_confirmed,
                          change_password,
                          send_confirm)
from ..tools import mail
from ..tools.decorators import log_error





log = logging.getLogger(__name__)
login_blueprint = Blueprint('login', __name__, template_folder='templates')

@login_blueprint.route("/login",methods=["GET","POST"])
@log_error
def client_login():
    '''Display and manage login form. '''

    loginForm = LoginForm()
    sender = 'lg@langdongreen.com'
    message = ''
    invalid = "Invalid form submission"
    confirmation_sent = "confirmation email sent to "
    login_error = "Incorrect email or password"
    
    action = 'login.client_login'
    button = 'login'
    #Form submitted validate and handle login or create new user.
    
    if loginForm.email.data and loginForm.password.data:
        if not loginForm.validate_on_submit():
            flash(invalid)
            return render_template('login.html', 
                                   action = action, loginForm = loginForm)
        else:
            email= loginForm.email.data
            password = loginForm.password.data

            #if user exists but is not confirmed
            if not user_confirmed(email):
                
                send_confirm(app.config.get('SECRET_KEY'),sender,[email])

                message = confirmation_sent
                
                return render_template('page.html', message = message)
                
            #if existing email, attempt to login
            elif user_exists(email):
    
                if login_user(email,password):

                    session['clientid'] = email
                    
                    if session['clientid']:
                        return redirect(url_for('user.user'))
                    
                    log.info(email+" logged in"+ " IP: " + request.remote_addr)
     
                else:
                    message = login_error
                    log.warning(email+" password didn't match"+ " IP: " +
                                request.remote_addr)
            #new client
            else:
                new_user(email,password)

                send_confirm(app.config.get('SECRET_KEY'),sender,[email])

                message = confirmation_sent

                return render_template('page.html', message = message)


    #render login form
    return render_template('login.html',
                           message = message,
                           action = action,
                           loginForm = loginForm,
                           button = button,
                           referrer = request.referrer)

def manage_user():
    '''Create a new user or login existing user
    Set session['clientid'] after successful login
    Add new user to database and send confirmation email'''
    
    
@login_blueprint.route("/logout/")
def client_logout():
    '''Logout client by clearing the session data, 
    redirect to logout message page'''
    message = ''
    try:
        log.info("User logged out IP: "+request.remote_addr)
        session.clear()
        session['clientid'] = ''
        g.user = ''
        g.admin = ''
        message = "Logged Out"
    except Exception as e:
        log.error("Logout exception  IP: " + request.remote_addr + " " + str(e))

    return render_template('page.html',message=message)


@login_blueprint.route("/update/<token>", methods=["GET","POST"])
@login_blueprint.route("/update/", methods=["GET","POST"])
def update_password(token=None):
    '''Accept token from link and display/manage password update form'''
    message = ''
    loginForm = LoginForm()
    success = "Password Updated"
    incorrect_input = "Passwords not the same"
    no_token = "Please submit your email at the reset password page"
    action = 'login.update_password'
    button = "Update"
    ts = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))
    
    #if form has been submitted check the token and change password
    if loginForm.validate_on_submit():
        
        email = ts.loads(loginForm.token.data, salt="updatekey", max_age=86400)
        if loginForm.password.data == loginForm.password2.data:
            change_password(email,loginForm.password.data)
            session['clientid'] = email
            log.info(email+" password update")
            message = success
        else:
            message = incorrect_input

    elif not token:
        message = no_token
        return render_template('page.html', message = message)
        
                #message = "Client Saved"
    return render_template('login.html',
                           token = token,
                           action=action,
                           loginForm = loginForm,
                           button=button,
                           referrer = request.referrer)


@login_blueprint.route("/reset", methods=["GET","POST"])
def reset_password():
    '''Get email address and send link to reset the users password (if existing)'''

    loginForm = LoginForm()
    message = ""
    success = "Email sent with instructions"
    action = "login.update_password"
    button = "Reset"
    if loginForm.send.data:
        #Clean and verify input
        if loginForm.validate() == False:
            flash("Invalid form submission")
            return render_template('login.html', 
                                   loginForm = loginForm,
                                   action = 'login.reset_password')
        else:
            ts = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))
            link = url_for('login.update_password',
                           _external = True,
                           token = ts.dumps(loginForm.email.data,salt='updatekey'))
            mail.send_email("Reset Password ",
                            app.config['ADMIN_EMAIL'],
                            [loginForm.email.data],link,'')
            message = success
            return render_template('page.html', message = message)

    return render_template('login.html',
                           message = message,
                           action = action,
                           loginForm = loginForm,
                           button = button,
                           referrer = request.referrer)


@login_blueprint.route("/confirm/<token>", methods=["GET","POST"])
def confirm_email(token):
    
    message = 'Email confirmed'
    
    try:
        ts = URLSafeTimedSerializer(app.config.get('SECRET_KEY'))
        email = ts.loads(token, salt="confirmationkey", max_age=86400)
        confirm_user(email)
        session['clientid'] = email
        log.info(email+" confirmed and logged in")
    except Exception as e:
        return render_template('page.html', message = 'confirm error')




    return render_template('page.html', message = message)
