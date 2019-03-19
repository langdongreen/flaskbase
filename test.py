import unittest

from base import app


class baseTestCase(unittest.TestCase):
    email = 'lg@langdongreen.com'
    password = 'sharnnee'
    user_path = '/user'
    login_path = '/login'
    logout_path = '/logout'
    
    invalid = "Invalid form submission"
    confirmation_sent = "confirmation email sent to "
    confirmation_message = "An email has been sent to confirm your address"
    login_error = "Incorrect email or password"
    
    def setUp(self):
        '''Setup test variables and remove form CSRF for easy submission'''
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['NOMAIL'] = False
        app.config['NODB'] = True
        
        self.client = app.test_client()

    def tearDown(self):
        '''anything required after testing'''
        pass

    def test_index(self):
        '''Test application home'''
        rv = self.client.get('/')
        assert b'index' in rv.data
  

    def test_login(self):
        '''test login,logout with correct and incorrect details'''
        #login correct user pass
        rv = self.login(self.email, self.password)
        print(rv.data)
        assert bytes(self.email,'utf-8') in rv.data
        
    def test_incorrect_password(self):
        #login incorrect password (incorrect user makes a new user)
        rv = self.login(self.email, self.password+'x')
        assert bytes(self.login_error,'utf-8') in rv.data
        
    def test_restricted(self):
        
        #test access to restricted pages

        rv = self.endpoint_get(self.user_path)
        assert b'Lost Password' in rv.data
        
        
        
        
    def test_new_user(self):
        #rv = self.login(self.email + 'x', self.password)
        #assert bytes('Lost Password',"utf-8") in rv.data
        pass
       

    def login(self, email, password):
        '''Post login details'''
        return self.client.post(self.login_path, 
                                data=dict(email=email,password=password),
                                follow_redirects=True)


    def logout(self):
        return self.client.get(self.logout_path, follow_redirects=True)

    def endpoint_get(self,endpoint,query=''):
        '''get an application endpoint'''
        return self.client.get(endpoint, query_string=query,follow_redirects=True)
    
    def endpoint_post(self,endpoint,post):
        '''post to an application endpoint'''
        return self.client.post(endpoint, data=post, follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
