import os
import unittest
import tempfile
import pytest
from flask import session, g
from app import app, login

class TestFlaskRoutes(unittest.TestCase):
    # check that flask set-up correctly at index
    def test_index_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/log-in', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_home_page_loads(self):
        g.user = 'test_user'
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_form_choice_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/choose_a_brew', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_brew_results_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/brew-results', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_add_profile_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/add_profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_add_recipe_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/add_recipe', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_my_brews_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/my_brews', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    # # test that login page renders correctly
    # def test_login_returns_correct_template(self):
    #     request = HttpRequest()
    #     response = tester.get('/log-in', content_type='html/text')
    #     html = response.content.decode('utf8')
    #     self.assertTrue(html.startswith('<html>'))
    #     self.assertIn('<title>Login Page</title>', html)
    #     self.assertTrue(html.endswith('</html>'))
        
    # test login behaves as expected with correct credentials
    
    # test login behaves as expected with incorrect credentials
    # def test_incorrect_login_redirect_working(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/log-in', ('username'!='valid_user'), follow_redirects=True)
    #     self.assertIn(b'*invalid login details', response.data)        
        
if __name__ == '__main__':
    unittest.main()
        