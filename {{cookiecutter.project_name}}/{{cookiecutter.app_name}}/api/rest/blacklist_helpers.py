from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from {{cookiecutter.app_name}}.extensions import db
from {{cookiecutter.app_name}}.models import TokenBlacklist
from {{cookiecutter.app_name}}.api.rest.exceptions import TokenNotFound


def add_token_to_database(encoded_token, identity_claim):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()


def get_user_tokens(user_identity):
    return TokenBlacklist.query.filter_by(user_identity=user_identity).all()


def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def revoke_token(token_id, user):
    try:
        token = TokenBlacklist.query.filter_by(
            id=token_id,
            user_identity=user
        ).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound as error:
        raise TokenNotFound("Token not found{}".format(token_id)) from error
