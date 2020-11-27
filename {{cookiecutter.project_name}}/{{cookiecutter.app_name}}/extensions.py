from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l("")
mail = Mail()
babel = Babel()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
