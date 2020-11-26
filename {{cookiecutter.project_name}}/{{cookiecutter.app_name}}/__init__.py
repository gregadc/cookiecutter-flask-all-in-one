import logging.config
from logging.handlers import SMTPHandler
from flask import Flask

from .extensions import db, mail, babel, migrate, login, ma, jwt
from .config import Config, LOGGING_CONFIG


def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app_context = app.app_context()
    app_context.push()

    registering_blueprints(app)
    configure_extensions(app)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                secure = None
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Mail Failure',
                credentials=auth, secure=secure)
            app.logger.addHandler(mail_handler)
        logging.config.dictConfig(LOGGING_CONFIG)
    return app


def registering_blueprints(app):
    from {{cookiecutter.app_name}}.main.views import bp as main_bp
    from {{cookiecutter.app_name}}.main.errors import bp as error_bp
    from {{cookiecutter.app_name}}.auth.views import bp as auth_bp
    from {{cookiecutter.app_name}}.api.rest.views import bp as api_bp
    from {{cookiecutter.app_name}}.api.graphql.views import bp as graphql_bp
    from {{cookiecutter.app_name}}.auth.google import google_bp
    from {{cookiecutter.app_name}}.auth.twitter import twitter_bp
    from {{cookiecutter.app_name}}.auth.facebook import facebook_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(graphql_bp)
    app.register_blueprint(google_bp, url_prefix="/login")
    app.register_blueprint(twitter_bp, url_prefix="/login")
    app.register_blueprint(facebook_bp, url_prefix="/login")


def configure_extensions(app):
    """configure flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
