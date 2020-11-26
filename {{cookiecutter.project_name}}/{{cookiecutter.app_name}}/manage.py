import click
from datetime import datetime as dt
from secrets import token_urlsafe
from flask.cli import FlaskGroup
from {{cookiecutter.app_name}} import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command('init')
def init():
    """ Init admin user """
    from {{cookiecutter.app_name}}.extensions import db
    from {{cookiecutter.app_name}}.models import User
    click.echo("Create DB")
    db.create_all()
    click.echo("create user")
    now = dt.now().replace(second=0, microsecond=0)
    user = User(
        username="admin",
        email="admin@gmail.com",
        created=now,
        token=token_urlsafe(),
        token_expiration=dt.now()
    )
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
