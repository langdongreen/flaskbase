from flask import url_for,request




def redirect_url(default='index'):
    '''Redirect user to previous page'''
    return request.args.get('next') or \
       request.referrer or \
       url_for('index')
