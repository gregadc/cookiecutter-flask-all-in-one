from datetime import datetime
from factory.alchemy import SQLAlchemyModelFactory
from factory import fuzzy, Sequence, LazyAttribute, LazyFunction

from app.extensions import db
from app.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = fuzzy.FuzzyInteger(1, 100)
    username = Sequence(lambda n: 'john%s' % n)
    email = LazyAttribute(lambda o: '%s@example.org' % o.username)
    created = LazyFunction(datetime.now)
    password = "password"
