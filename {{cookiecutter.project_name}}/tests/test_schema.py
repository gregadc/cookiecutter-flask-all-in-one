import json
import unittest
from graphene.test import Client

from {{cookiecutter.app_name}}.api.graphql.views import schema
from {{cookiecutter.app_name}}.config import Config
from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}} import create_app as app
from tests import factories

QUERY_USER_ID = """
{
  users(userId:%d){
    edges{
      node{
        email
        username
        created
      }
    }
  }
}
"""

QUERY_ALL_USERS = """
{
  users(sort: USERNAME_ASC){
    edges{
      node{
        email
        username
        created
      }
    }
  }
}
"""


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserSchemaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app(TestConfig)
        db.create_all()
        self.client = Client(schema)
        self.user_factory = factories.UserFactory.create_batch(10)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_user(self):
        user = self.user_factory[0]
        query = QUERY_USER_ID % (user.id)
        res = self.client.execute(query)
        self.assertIn(user.email, json.dumps(res))
        self.assertEqual(1, len(res['data']['users']['edges']))

    def test_get_all_users(self):
        res = self.client.execute(QUERY_ALL_USERS)
        self.assertEqual(10, len(res['data']['users']['edges']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
