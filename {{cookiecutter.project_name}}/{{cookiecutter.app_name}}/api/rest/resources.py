from flask import request, url_for, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from {{cookiecutter.app_name}}.extensions import db, jwt
from {{cookiecutter.app_name}}.models import User
from {{cookiecutter.app_name}}.api.rest.schemas import UserSchema

PER_PAGE = 50
PAGE_NUMBER = 1

SETTING_PAG = {
    "page": PAGE_NUMBER,
    "per_page": PER_PAGE
}


def is_digit(value, argument_name):
    if isinstance(value, int):
        return value
    elif isinstance(value, float) or value.isdigit():
        return int(value)
    try:
        value = float(value)
        return int(value)
    except ValueError:
        return SETTING_PAG[argument_name]


def paginate(query, schema):
    page = is_digit(request.args.get('page', PAGE_NUMBER), 'page')
    per_page = is_digit(request.args.get('per_page', PER_PAGE), 'per_page')
    page_obj = query.paginate(page=page, per_page=per_page)
    has_next = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=per_page,
        **request.view_args
    )
    has_prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=per_page,
        **request.view_args
    )

    return {
        'total': page_obj.total,
        'pages': page_obj.pages,
        'has_next': has_next,
        'has_prev': has_prev,
        'current_page': page_obj.page,
        'data': schema.dump(page_obj.items)
    }


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):
        schema = UserSchema()
        user = User.query.filter_by(id=user_id).first_or_404()
        return schema.dump(user)

    @jwt_required
    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=user_id).first_or_404()
        user = schema.load(request.json, instance=user)
        db.session.commit()
        return {"User updated": schema.dump(user)}


class UserListResource(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    @jwt_required
    def post(self):
        schema = UserSchema(partial=True)
        user = schema.load(request.json)
        db.session.add(user)
        db.session.commit()
        return {"User created": schema.dump(user)}
