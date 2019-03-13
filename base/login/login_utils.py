from ..tools import sdb
from argon2 import PasswordHasher
from base import c,logging

def user_exists(user):
    '''Check to make sure user item is in sdb'''
    try:
        item = sdb.get_attributes(c['domain'],user)
        if item['Attributes']:
            return True;
        
    except Exception as e:
        logging.error(e)
        return None


def new_user(user,password):
    '''Add new user item and password attribute to sdb'''
    hash = hash_password(password)

    try:
        sdb.add_attribute(c['domain'],user,('confirmed','0'))
        sdb.add_attribute(c['domain'],user,('password',hash))
        return True
    except KeyError as e:
        logging.error(e)
        return False
    

def confirm_user(user):
    '''Confirm users email is valid'''
    if user_exists(user):
     return sdb.add_attribute(c['domain'],user,('confirmed','1'))
 
def user_confirmed(user):
    '''check if user item has been confirmed'''
  
    try:
        items = sdb.get_attributes(c['domain'],user)['Attributes']
        logging.debug(next(item for item in items if item["Name"] == "confirmed"))
        if next(item['Value'] for item in items if item["Name"] == "confirmed") == '1':
            return True
        else:
            return False
    except Exception as e:
        logging.debug(e)
        return None
               

def delete_user(user):
    '''delete user item from sdb'''
    pass

def change_password(user,password):
    '''update sdb user item with new password'''
    hash = hash_password(password)
    sdb.add_attribute(c['domain'],user,('password',hash))

def login_user(user,input):
    '''Retrieve user item and password attribute from sdb and check password'''
    password = sdb.get_attributes(c['domain'],user)

    logging.debug(password)
    if password:
        password = password['Attributes'][0]['Value']

    return check_password(input,password)

def check_password(input,password):
    '''check entered password with the password attribute in sdb'''
    ph = PasswordHasher()
    try:
        ph.verify(password,input)
    except Exception as e:
        logging.error(e)
        return False

    return True

def hash_password(password):
    '''Hash password with argon2'''
    ph = PasswordHasher()
    return ph.hash(password)
