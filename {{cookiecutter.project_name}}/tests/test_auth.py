from datetime import timedelta
import json
import unittest

from {{cookiecutter.app_name}} import create_app as app
from {{cookiecutter.app_name}}.config import Config
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.models import TokenBlacklist
from tests import factories


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app(TestConfig)
        db.create_all()
        self.factory = factories.UserFactory.create()
        self.client = self.app.test_client

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTestCase(BaseCase):

    def test_change_password(self):
        self.factory.set_password('test')
        self.assertTrue(self.factory.check_password('test'))

    def test_token_expiration(self):
        token = self.factory.token
        self.factory.token_expiration =  \
            self.factory.token_expiration - timedelta(minutes=60)
        self.factory.verify_expiration_token()
        self.assertNotEqual(self.factory.token, token)

    def test_not_logged(self):
        tester = self.client()
        res = tester.get('/index', content_type='html/text')
        self.assertEqual(res.status_code, 302)

    def test_login(self):
        tester = self.client()
        res = tester.post(
            '/auth/login',
            data=dict(username=self.factory.username, password='password'),
            follow_redirects=True
        )
        value = "Welcome {0}".format(self.factory.username.capitalize())
        self.assertEqual(res.status_code, 200)
        self.assertIn(value, res.data.decode())

    def test_register_user(self):
        tester = self.client()
        data = {
            "username": self.factory.username,
            "email": self.factory.email,
            "password": "password",
            "password2": "password"
        }
        # Register User
        res = tester.post(
            '/auth/register',
            data=json.dumps(data),
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)
        # Login new user
        res = tester.post(
            '/auth/login',
            data=dict(username=self.factory.username, password='password'),
            follow_redirects=True
        )
        value = "Welcome {0}".format(self.factory.username.capitalize())
        self.assertEqual(res.status_code, 200)
        self.assertIn(value, res.data.decode())


    def test_token_process(self):
        tester = self.client()
        # Create tokens
        res = tester.post(
            '/api/login',
            data=json.dumps(dict(
                username=self.factory.username,
                password='password')
            ),
            headers={'content-type': 'application/json'}
        )
        tokens = json.loads(res.get_data(as_text=True))
        header_token = {
            'content-type': 'application/json',
            'authorization': 'Bearer %s' % tokens['access_token']
        }
        self.assertEqual(res.status_code, 201)
        # Get tokens
        res = tester.get('/api/tokens', headers=header_token)
        self.assertEqual(res.status_code, 200)
        token_id = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        token_id = TokenBlacklist.query.first().to_dict['token_id']
        # Revoke token
        res = tester.delete(
            '/api/revoke_token/{0}'.format(token_id),
            headers=header_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual({'message': 'token revoked'}, json.loads(res.data))

    def test_refresh_token(self):
        tester = self.client()
        # Create tokens
        res = tester.post(
            '/api/login',
            data=json.dumps(dict(
                username=self.factory.username,
                password='password')
            ),
            headers={'content-type': 'application/json'}
        )
        tokens = json.loads(res.get_data(as_text=True))
        header_token = {
            'content-type': 'application/json',
            'authorization': 'Bearer %s' % tokens['refresh_token']
        }
        self.assertEqual(res.status_code, 201)
        # Refresh token
        res = tester.post('/api/refresh', headers=header_token)
        self.assertEqual(res.status_code, 201)


if __name__ == '__main__':
    unittest.main(verbosity=2)
