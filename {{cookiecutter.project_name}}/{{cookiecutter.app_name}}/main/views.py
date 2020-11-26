import logging
from flask import render_template, Blueprint, make_response, current_app as app
from flask_login import login_required

from {{cookiecutter.app_name}}.models import User

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__, url_prefix="/", static_folder="../static")


@bp.route("/", methods=['GET'])
@bp.route("/index", methods=['GET'])
@login_required
def index():
    return render_template(
        'main/index.html',
        users=User.query.all()
    )


@bp.route("/rest_rules", methods=['GET'])
@login_required
def rest_rules():
    rules = ""
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/api'):
            rules += "{0} {1}\n".format(rule, rule.methods)
    response = make_response(rules)
    response.headers["content-type"] = "text/plain"
    return response
