# -*- coding: utf-8 -*-
"""The api v1.0 module."""

from flask import Blueprint
from flask.ext.restful import Api

api_blueprint = Blueprint("api", __name__, url_prefix='/api/v1.0')
api = Api(api_blueprint)


from just.resources.v1_0.wechat import menu # noqa
