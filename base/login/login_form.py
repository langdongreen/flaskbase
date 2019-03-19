from flask_wtf import Form
from wtforms import (SubmitField,
                     PasswordField, 
                     HiddenField,
                     validators)
from wtforms.fields.html5 import EmailField


class LoginForm(Form):
    email = EmailField('email',[validators.Email("Please enter your email address.")])
    password = PasswordField('password')
    password2 = PasswordField('password again')
    token = HiddenField()
    send = SubmitField('Login')
