from flask_wtf import Form
from wtforms import StringField, SubmitField,PasswordField, HiddenField

class LoginForm(Form):
    email = StringField('email')
    password = PasswordField('password')
    password2 = PasswordField('password again')
    token = HiddenField()
    send = SubmitField('Login')
