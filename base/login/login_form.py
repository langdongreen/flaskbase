from flask_wtf import Form
from wtforms import StringField, SubmitField,PasswordField, validators,HiddenField

class LoginForm(Form):
    email = StringField('email')
    password = PasswordField('password')
    password2 = PasswordField('password again')
    token = HiddenField()
    send = SubmitField('Login')

class UpdatePassword(Form):
    password = PasswordField('password', [validators.Required("Please enter a password")])
    send = SubmitField('Update Password')

class ResetForm(Form):
    email = StringField('email',[validators.Required("Please enter an email address"), validators.Email("Valid email address required")])
    send = SubmitField('Send Email')
