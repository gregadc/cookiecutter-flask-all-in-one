import json
import unittest
from sqlalchemy import asc
from graphene.test import Client

from app.api.graphql.views import schema
from app.config import Config
from app.extensions import db
from app import create_app as app
from tests import factories

QUERY_USER_ID = """
{{
  users(userId:{0}){{
    edges{{
      node{{
        email
        username
        created
      }}
    }}
  }}
}}
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
        res = self.client.execute(QUERY_USER_ID.format(user.id))
        self.assertIn(user.email, json.dumps(res))
        self.assertEqual(1, len(res['data']['users']['edges']))

    def test_get_all_users(self):
        res = self.client.execute(QUERY_ALL_USERS)
        self.assertEqual(10, len(res['data']['users']['edges']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
