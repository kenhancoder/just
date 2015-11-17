# -*- coding: utf-8 -*-
"""The api module, containing the api factory function."""
from flask.ext.restful import Api
from just.resources.v1_0 import version
from just.resources.v1_0.wechat import Menu


def create_api(app):

    api = Api(app)
    add_resource(api)


def add_resource(api):

    api.add_resource(Menu, '/api/{0}/menus'.format(version))
