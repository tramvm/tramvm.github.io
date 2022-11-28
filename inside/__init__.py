
# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template
from flask.ext.babel import Babel
from flask.ext.login import current_user

from inside import utils
from inside.models import User
from inside.config import DefaultConfig, APP_NAME
from inside.views import site
from inside.extensions import db, mail, login_manager, sentry_client #, task_client
from inside import extensions
#from inside.libs.rsession import RedisSessionInterface
from raven.middleware import Sentry


# For import *
#__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    site,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = APP_NAME
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)
    configure_app(app, config)
    configure_blueprints(app, blueprints)

    configure_extensions(app)
    configure_hook(app)
#    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config):
    """Configure app from object, parameter and env."""

    app.config.from_object(DefaultConfig)
    if config is not None:
        app.config.from_object(config)
    # Override setting by env var without touching codes.
    app.config.from_envvar('FBONE_APP_CONFIG', silent=True)


def configure_extensions(app):
    #app.session_interface = RedisSessionInterface()
    # sqlalchemy
    db.init_app(app)

    # mail
    #mail.init_app(app)

    # cache
    #cache.init_app(app)

    # babel
    babel = Babel(app, default_timezone='Asia/Ho_Chi_Minh')

    # Cloud task client
    #task_client.init_app(app)

    sentry = Sentry(app, sentry_client)


    # login.
    login_manager.login_view = 'site.login'
    login_manager.refresh_view = 'site.reauth'

    @login_manager.user_loader
    def load_user(login):
        return db.User.find_user(login)

    login_manager.setup_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):
    app.jinja_env.globals.update(u=current_user)
    @app.template_filter()
    def pretty_date(value):
        return utils.pretty_date(value)
    @app.template_filter('url_external')
    def url_external(value):
        return utils.url_external(value)
    @app.template_filter('break_line_html')
    def break_line_html(value):
        return utils.break_line_html(value)
    @app.template_filter('slugit')
    def slugit(value):
        return utils.slugit(value)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # skip debug and test mode.
        return

    import logging
    from logging.handlers import RotatingFileHandler, SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    app.logger.setLevel(logging.INFO)

    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    file_handler = logging.handlers.RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(file_handler)


def configure_hook(app):
    pass
    # @app.before_request
    # def before_request():
    #     public_endpoint = ['static', 'site.login', 'site.logout', 'site.locale']
    #     if request.endpoint not in public_endpoint and not current_user.is_authenticated():
    #         return current_app.login_manager.unauthorized()


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        print "------------------------- error ---------------------------"
        return render_template("errors/server_error.html"), 500

inside = create_app()
