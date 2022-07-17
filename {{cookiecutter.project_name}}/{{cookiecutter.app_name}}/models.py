from datetime import datetime, timedelta
from secrets import token_urlsafe
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from {{cookiecutter.app_name}}.extensions import db, login

DATE = datetime.now().replace(second=0, microsecond=0)


class User(db.Model, UserMixin):
    """Data model for user accounts."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=False, unique=False, nullable=False)
    email = db.Column(db.String(80), index=True, unique=False, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(80), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    oauth = db.relationship("OAuth", back_populates="user", uselist=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.created = DATE
        self.token = token_urlsafe()
        self.token_expiration = DATE
        self.password = ""

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def to_dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'created': str(self.created),
        }

    def verify_expiration_token(self):
        now = datetime.now()
        if now > self.token_expiration + timedelta(minutes=60):
            self.token = token_urlsafe()
            self.token_expiration = now
        return self.token


class OAuth(OAuthConsumerMixin, db.Model):
    """Data model for oauth accounts."""

    __tablename__ = 'oauth'

    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship("User", back_populates="oauth", uselist=False)


class TokenBlacklist(db.Model):

    __tablename__ = 'tokenblacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    @property
    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
