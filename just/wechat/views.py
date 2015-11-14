# -*- coding: utf-8 -*-
"""Wechat views."""

from wechat_sdk import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage

from flask import request, Blueprint, render_template

blueprint = Blueprint('wechat', __name__, static_folder='../static')


@blueprint.route('/wechat', methods=['POST', 'GET'])
def wechat():
    """HOME PAGE"""
    # return render_template('public/home.html')
    import os
    from ConfigParser import ConfigParser
    config = ConfigParser()
    this_dir = os.path.dirname(__file__)
    config.read(os.path.join(this_dir, 'wechat.cfg'))

    cfg = 'PROD' if os.environ.get('JUST_ENV') == 'prod' else 'DEV'
    token = config.get(cfg, 'TOKEN')
    appid = config.get(cfg, 'APPID')
    appsecret = config.get(cfg, 'APPSECRET')

    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    # 实例化 wechat
    wechat = WechatBasic(token=token, appid=appid, appsecret=appsecret)

    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return 'fail'

    # 验证服务器地址的有效性
    echostr = request.args.get('echostr')
    if echostr:
        return echostr

    wechat.parse_data(request.data)
    message = wechat.get_message()

    if isinstance(message, TextMessage):
        response = wechat.response_text(content=u'文字信息')
    elif isinstance(message, VoiceMessage):
        response = wechat.response_text(content=u'语音信息')
    elif isinstance(message, ImageMessage):
        response = wechat.response_text(content=u'图片信息')
    elif isinstance(message, VideoMessage):
        response = wechat.response_text(content=u'视频信息')
    elif isinstance(message, LinkMessage):
        response = wechat.response_text(content=u'链接信息')
    elif isinstance(message, LocationMessage):
        response = wechat.response_text(content=u'地理位置信息')
    elif isinstance(message, EventMessage):  # 事件信息
        # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
        if message.type == 'subscribe':
            response = wechat.response_text(content=u'关注信息')
        elif message.type == 'unsubscribe':
            response = wechat.response_text(content=u'取消关注信息')
        elif message.type == 'scan':
            response = wechat.response_text(content=u'扫描二维码信息')
        elif message.type == 'location':
            response = wechat.response_text(content=u'获取地理位置信息')
        elif message.type == 'click':
            response = wechat.response_text(content=u'点击')
        elif message.type == 'view':
            response = wechat.response_text(content=u'跳转信息')
        elif message.type == 'templatesendjobfinish':
            response = wechat.response_text(content=u'模板消息事件')
    return response
