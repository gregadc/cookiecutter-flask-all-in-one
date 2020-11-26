from flask import Blueprint
from flask_graphql import GraphQLView
from flask_login import login_required

from {{cookiecutter.app_name}}.api.graphql.schemas import schema

bp = Blueprint('graphql', __name__)


def graphql():
    view = GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    return login_required(view)


bp.add_url_rule('/graphql', view_func=graphql())
