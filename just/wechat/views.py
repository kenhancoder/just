# -*- coding: utf-8 -*-
"""Wechat views."""

import os
import time
from ConfigParser import ConfigParser

from wechat_sdk import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage

from flask import request, Blueprint, render_template

config = ConfigParser()
this_dir = os.path.dirname(__file__)
config.read(os.path.join(this_dir, 'wechat.cfg'))
cfg = 'PROD' if os.environ.get('JUST_ENV') == 'prod' else 'DEV'
token = config.get(cfg, 'TOKEN')
appid = config.get(cfg, 'APPID')
appsecret = config.get(cfg, 'APPSECRET')
# 实例化 wechat
wechat_entity = WechatBasic(token=token, appid=appid, appsecret=appsecret)


blueprint = Blueprint('wechat', __name__)


@blueprint.route('/wechat', methods=['POST', 'GET'])
def wechat():
    """WECHAT"""

    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    # 对签名进行校验
    if not wechat_entity.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return 'fail'

    # 验证服务器地址的有效性
    echostr = request.args.get('echostr')
    if echostr:
        return echostr

    # 更新 access_token
    cache_access_token_info = wechat_entity.get_access_token()
    expries_at = cache_access_token_info.get('access_token_expires_at', None)
    if expries_at is None or expries_at < int(time.time()):
        wechat_entity.grant_token()

    wechat_entity.parse_data(request.data)
    message = wechat_entity.get_message()

    if isinstance(message, TextMessage):
        response = wechat_entity.response_text(content=u'文字信息')
    elif isinstance(message, VoiceMessage):
        response = wechat_entity.response_text(content=u'语音信息')
    elif isinstance(message, ImageMessage):
        response = wechat_entity.response_text(content=u'图片信息')
    elif isinstance(message, VideoMessage):
        response = wechat_entity.response_text(content=u'视频信息')
    elif isinstance(message, LinkMessage):
        response = wechat_entity.response_text(content=u'链接信息')
    elif isinstance(message, LocationMessage):
        response = wechat_entity.response_text(content=u'地理位置信息')
    elif isinstance(message, EventMessage):  # 事件信息
        # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
        if message.type == 'subscribe':
            response = wechat_entity.response_text(content=u'关注信息')
        elif message.type == 'unsubscribe':
            response = wechat_entity.response_text(content=u'取消关注信息')
        elif message.type == 'scan':
            response = wechat_entity.response_text(content=u'扫描二维码信息')
        elif message.type == 'location':
            response = wechat_entity.response_text(content=u'获取地理位置信息')
        elif message.type == 'click':
            response = wechat_entity.response_text(content=u'点击')
        elif message.type == 'view':
            response = wechat_entity.response_text(content=u'跳转信息')
        elif message.type == 'templatesendjobfinish':
            response = wechat_entity.response_text(content=u'模板消息事件')
    return response
