# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask.ext.restful import Api
from flask import Flask, render_template

from just import public, wechat
from just.resources.v1_0 import api_blueprint
from just.assets import assets
from just.extensions import bcrypt, cache, db, debug_toolbar, migrate
from just.settings import ProdConfig

global api

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    import os
    if os.environ.get('JUST_ENV') in (None, 'dev'):
        debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    app.register_blueprint(wechat.views.blueprint)
    # app.register_blueprint(api.views.blueprint)
    app.register_blueprint(api_blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
