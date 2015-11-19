# -*- coding: utf-8 -*-
"""The wechat api v1 menu module."""

import time

from flask.ext.restful import Resource, fields

from just.resources.v1_0 import api
from just.wechat import wechat_entity

# menus_fields = {
#     'button': fields.List(


#         )


# }

menus = {
    'button': [
        {
            'type': 'click',
            'name': '今日歌曲',
            'key': 'V1001_TODAY_MUSIC'
        },
        {
            'type': 'click',
            'name': '歌手简介',
            'key': 'V1001_TODAY_SINGER'
        },
        {
            'name': '菜单',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '搜索',
                    'url': 'http://www.soso.com/'
                },
                {
                    'type': 'view',
                    'name': '视频',
                    'url': 'http://v.qq.com/'
                },
                {
                    'type': 'click',
                    'name': '赞一下我们',
                    'key': 'V1001_GOOD'
                }
            ]
        }
    ]
}

@api.resource('/menus')
class Menu(Resource):
    """Wechat Menu Resource"""

    def __init__(self):
        self.wechat = wechat_entity

    def check_access_token(self):
        # 更新 access_token
        cache_access_token_info = self.wechat.get_access_token()
        expries_at = cache_access_token_info.get(
            'access_token_expires_at', None)
        if expries_at is None or expries_at < int(time.time()):
            self.wechat.grant_token()

    def get(self):
        self.check_access_token()
        return self.wechat.get_menu()

    def post(self):
        self.check_access_token()
        return self.wechat.create_menu(menus)

        pass
