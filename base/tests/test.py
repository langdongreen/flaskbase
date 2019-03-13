from base import app,c

import unittest

class baseTestCase(unittest.TestCase):
    email = 'email@address'
    password = 'password'
    admin = '/admin'
    login = '/login'
    logout = '/logout'

    def setUp(self):
        '''Setup test variables and remove form CSRF for easy submission'''
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['NOMAIL'] = False
        app.config['NODB'] = True

        
        self.app = app.test_client()

    def tearDown(self):
        '''anything required after testing'''
        pass

    def test_index(self):
        '''Test application home'''
        rv = self.app.get('/')
        assert b'' in rv.data

    def test_login(self):
        '''test login,logout with correct and incorrect details'''

        rv = self.login(self.email, self.password)
        assert b'Admin' in rv.data

        rv = self.logout()
        assert bytes(c['messages']['logout_message'],"utf-8") in rv.data

        rv = self.login(self.email + 'x', self.password)
        assert bytes('Lost Password',"utf-8") in rv.data

        rv = self.logout()
        assert bytes(c['messages']['logout_message'],"utf-8") in rv.data

        rv = self.login(self.email, self.password+'x')
        assert bytes(c['messages']['login_error'],"utf-8") in rv.data

       

    def login(self, email, password):
        '''Post login details'''
        return self.app.post(self.login, data=dict(
        email=email,
        password=password
         ), follow_redirects=True)


    def logout(self):
        return self.app.get(self.logout, follow_redirects=True)

    def endpoint_get(self,endpoint,query=''):
        '''get an application endpoint'''
        return self.app.get(endpoint, query_string=query,follow_redirects=True)
    
    def endpoint_post(self,endpoint,post):
        '''post to an application endpoint'''
        return self.app.post(endpoint, data=post, follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
