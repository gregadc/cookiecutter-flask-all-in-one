from app.extensions import db, ma
from app.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        load_instance = True
        sqla_session = db.session
        model = User
