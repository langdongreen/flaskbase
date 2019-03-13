'''Perform user creation and login functions for application'''

from flask import render_template, request, flash, session,url_for, redirect, g
import logging
from base import app,c,ts
from .login_form import LoginForm
from .login_utils import user_exists,login_user,new_user,confirm_user,user_confirmed,change_password
from ..tools import mail


@app.route("/login",methods=["GET","POST"])
def client_login():
    '''Display and manage login form.  Create a new user or login existing user
    Set session['clientid'] after successful login
    Add new user to database and send confirmation email'''

    loginForm = LoginForm()
    message = ''
    action = 'client_login'
    #Form submitted validate and handle login or create new user.
    if loginForm.email.data and loginForm.password.data:
        if not loginForm.validate():
            flash("Invalid form submission")
            return render_template('login.html', action = action, loginForm = loginForm)
        else:
            email= loginForm.email.data
            password = loginForm.password.data

            #if user exists but is not confirmed
            if not user_confirmed(email):
                link = url_for('confirm_email', _external = True, token = ts.dumps(loginForm.email.data,salt='confirmationkey'))
                mail.send_email("Confirm Email ",c['admin'],[loginForm.email.data],link,'')
                logging.debug(user_confirmed(email))
                
                message = c['messages']['confirmation_email']
                logging.info("Sent confirmation email to " +email + " IP: " + request.remote_addr)

                return render_template('page.html', message = message)
                
            #if existing email, attempt to login
            elif user_exists(email):
    
                if login_user(email,password):

                    session['clientid'] = email

                    logging.info(email+" logged in"+ " IP: " + request.remote_addr)
                    if session['clientid']:
                        return redirect(url_for('user'))
                    else:
                        return redirect(url_for('client_login'))

                else:
                    message = c['messages']['login_error']
                    logging.warning(email+" password didn't match"+ " IP: " + request.remote_addr)
            #new client
            else:
                if new_user(email,password):

                    link = url_for('confirm_email', _external = True, token = ts.dumps(loginForm.email.data,salt='confirmationkey'))
                    mail.send_email("Confirm Email ",c['admin'],[loginForm.email.data],link,'')

                    message = c['messages']['confirmation_email']
                    logging.info("Sent confirmation email to " +email + " IP: " + request.remote_addr)

                    return render_template('page.html', message = message)
                else:
                        render_template('page.html', message = "Not a user")

    return render_template('login.html', message = message, action = action, loginForm = loginForm, referrer = request.referrer)

@app.route("/logout/")
def client_logout():
    '''Logout client by clearing the session data, redirect to logout message page'''
    message = ''
    try:
        logging.info("User logged out IP: "+request.remote_addr)
        session.clear()
        session['clientid'] = ''
        g.user = ''
        g.admin = ''
        message = c['messages']['logout_message']
    except Exception as e:
        logging.error("Logout exception  IP: " + request.remote_addr + " " + str(e))

    return render_template('page.html',message=message)


@app.route("/update/<token>", methods=["GET","POST"])
@app.route("/update/", methods=["GET","POST"])
def update_password(token=None):
    '''Accept token from link and display/manage password update form'''
    loginForm = LoginForm()
   
    #if form has not been submitted and data checks out, display update form
    if not loginForm.send.data:
        try:
            email = ts.loads(token, salt="updatekey", max_age=86400)
            render_template('login.html',action = 'update_password', loginForm = loginForm,token=token)
        except Exception as e:
            return render_template('page.html', message = e)
    else:
        email = ts.loads(loginForm.token.data, salt="updatekey", max_age=86400)
        password = loginForm.password.data
        change_password(email,password)
        session['clientid'] = email
        logging.info(email+" password update")
        

                #message = "Client Saved"
    return render_template('login.html', token = token,action='update_password',loginForm = loginForm, referrer = request.referrer)


@app.route("/reset", methods=["GET","POST"])
def reset_password():
    '''Get email address and send link to reset the users password (if existing)'''

    loginForm = LoginForm()
    message = ''
    if loginForm.send.data:
        #Clean and verify input
        if loginForm.validate() == False:
            flash("Invalid form submission")
            return render_template('login.html', loginForm = loginForm,action = 'reset_password')
        else:
            link = url_for('update_password', _external = True, token = ts.dumps(loginForm.email.data,salt='updatekey'))
            mail.send_email("Reset Password ",c['admin'],[loginForm.email.data],link,'')
            #if existing email, email with reset link, otherwise do nothing.

            return render_template('page.html', message = c['update_password_sent'])

    return render_template('login.html',message = message, action = 'reset_password', loginForm = loginForm,referrer = request.referrer)


@app.route("/confirm/<token>", methods=["GET","POST"])
def confirm_email(token):
    try:
        email = ts.loads(token, salt="confirmationkey", max_age=86400)
        confirm_user(email)
        session['clientid'] = email
        logging.info(email+" confirmed and logged in")
    except Exception as e:
        return render_template('page.html', message = e)




    return render_template('page.html', message = c['messages']['email_confirmed'])
