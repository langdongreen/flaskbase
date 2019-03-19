import logging

from flask import url_for
from passlib.hash import bcrypt
from itsdangerous import URLSafeTimedSerializer

from ..tools import sdb
from base.tools import mail

log = logging.getLogger(__name__)

domain = 's3mail'


def user_exists(user):
    '''Check to make sure user item is in sdb'''

    item = sdb.select_id(domain,user)

    if 'Items' in item:
        return True
    else:
        return False
  
 


def new_user(user,password):
    '''Add new user item and password attribute to sdb'''
    hash = hash_password(password)
        
    sdb.add_attribute(domain,user,('confirmed','0'))
    sdb.add_attribute(domain,user,('password',hash))

    
    

def send_confirm(key,sender,recipient):
    ts = URLSafeTimedSerializer(key)
    link = url_for('login.confirm_email', 
                   _external = True,
                   token = ts.dumps(recipient,salt='confirmationkey'))
    mail.send_email("Confirm Email ",sender,recipient,link,'')
  

def confirm_user(user):
    '''Confirm users email is valid'''
 
    if user_exists(user):
     return sdb.add_attribute(domain,user,('confirmed','1'))

def user_confirmed(user):
    '''check if user item has been confirmed'''
    try:
        items = sdb.get_attributes(domain,user)['Attributes']
    
        if next(item['Value'] for item in items if item["Name"] == "confirmed") == '1':
            return True
    except KeyError:
            return False

               

def delete_user(user):
    '''delete user item from sdb'''
    pass

def change_password(user,password):
    '''update sdb user item with new password'''
    if user_exists(user):
        hash = hash_password(password)
        sdb.add_attribute(domain,user,('password',hash))

def login_user(user,input):
    '''Retrieve user item and password attribute from sdb and check password'''
    password = sdb.get_attributes(domain,user)

    if 'Attributes' in password:
        password = password['Attributes'][0]['Value']

    return check_password(input,password)

def check_password(input,password):
    '''check entered password with the password attribute in sdb'''
    return bcrypt.verify(input,password)


def hash_password(password):
    '''Hash password with argon2'''
    return bcrypt.hash(password)