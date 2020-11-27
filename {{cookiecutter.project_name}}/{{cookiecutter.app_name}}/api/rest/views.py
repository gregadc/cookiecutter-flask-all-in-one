import datetime

from flask import Blueprint, request, jsonify, current_app as app
from flask_restful import Api
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    create_refresh_token
)

from {{cookiecutter.app_name}}.api.rest.blacklist_helpers import (
    is_token_revoked,
    add_token_to_database,
    get_user_tokens,
    revoke_token
)
from {{cookiecutter.app_name}}.api.rest.resources import UserResource, UserListResource
from {{cookiecutter.app_name}}.extensions import jwt
from {{cookiecutter.app_name}}.models import User

bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@bp.app_errorhandler(404)
def handle_404(err):
    return jsonify({"mgs": "{0}".format(err)}), 404


@bp.app_errorhandler(500)
def handle_500(err):
    return jsonify({"mgs": "{0}".format(err)}), 500


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password parameter"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "You are not registered"}), 401

    expires = datetime.timedelta(minutes=20)
    access_token = create_access_token(
        identity=user.username,
        expires_delta=expires
    )
    refresh_token = create_refresh_token(identity=user.username)

    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

    ret = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonify(ret), 201


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify({'access_token': access_token}), 201


@bp.route('/tokens', methods=['GET'])
@jwt_required
def get_tokens():
    user_identity = get_jwt_identity()
    all_tokens = get_user_tokens(user_identity)
    ret = [token.to_dict for token in all_tokens]
    return jsonify(ret), 200


@bp.route('/revoke_token/<token_id>', methods=['DELETE'])
@jwt_required
def revoke(token_id):
    user_identity = get_jwt_identity()
    revoke_token(token_id, user_identity)
    return jsonify({"message": "token revoked"}), 200
