from {{cookiecutter.app_name}}.extensions import db, ma
from {{cookiecutter.app_name}}.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        load_instance = True
        sqla_session = db.session
        model = User
