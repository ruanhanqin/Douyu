#!/usr/bin/env python
# -*-encoding: utf-8-*-

"""
get the lottery room Id

query_url = 'https://www.douyu.com/member/recommlist/getfreshlistajax? \
            click_num=6&did=8478e9bd0ebff4b53df1b0d600021501&type=2&show_num=4&bzdata=0'
method:GET

query_data = {
    'bzdata': '0',# default 0
    'click_num': '1', # Increment by one
    'did': '8478e9bd0ebff4b53df1b0d600021501', # default # 登录用户的id
    'show_num': '4', # default 4
    'type': '2' # default 2
}
"""

from json import loads


class GetLotteryRoomId(object):
    """
    获取有抽奖的房间号
    """

    def __init__(self, session):
        self.session = session
        self.default_url = '''https://www.douyu.com/member/recommlist/getfreshlistajax?
                                   click_num={}&did={}&type={}&show_num={}&bzdata={}'''
        self.url = ''

    def get_room_id(self, click_num):
        """
        获取房间信息
        :param click_num:  点击次数，递增
        :return:
        """
        did = '8478e9bd0ebff4b53df1b0d600021501'
        room_list = []
        self.url = self.default_url.format(click_num, did, '2', '4', '0')
        response = self.session.get(self.url)
        if response.status_code == 200:
            if response.text:
                res_json = loads(response.text)
                for i in range(5):  # 10 ,一次返回10条房间数据(有时候没有那么多，改成5）
                    try:
                        room_id = res_json['room'][i]['room_id']  # 房间ID
                        room_name = res_json['room'][i]['room_name']  # 房间名
                        room_info = dict()
                        room_info['room_id'] = room_id
                        room_info['room_name'] = room_name
                        room_list.append(room_info)
                    except Exception as e:
                        print('getLotteryRoomId:', e)
                        return None
                return room_list
        else:
            return None
