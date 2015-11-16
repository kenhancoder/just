# -*- coding: utf-8 -*-
"""Wechat views."""

from wechat_sdk import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage

from flask import request, Blueprint, render_template

blueprint = Blueprint('api', __name__)


@blueprint.route('/api', methods=['POST', 'GET'])
def api():
    """API reflect"""
    # return render_template('public/home.html')
    pass
