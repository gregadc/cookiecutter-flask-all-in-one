import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from {{cookiecutter.app_name}}.models import User


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = SQLAlchemyConnectionField(
        UserSchema.connection,
        user_id=graphene.Int(),
        sort=UserSchema.sort_argument()

    )

    def resolve_users(self, info, user_id=None, **kwargs):
        query = UserSchema.get_query(info=info)
        if user_id:
            query = query.filter(User.id == user_id)
        return query.all()


schema = graphene.Schema(query=Query)
