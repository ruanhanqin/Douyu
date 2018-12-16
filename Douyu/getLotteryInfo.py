#!/usr/bin/env python
# -*-encoding: utf-8-*-

"""
get lottery information  by room Id

query_url = 'https://www.douyu.com/member/lottery/activity_info?t=1529227771124&room_id=3977230'

method:GET

query_data = {
    'room_id': room_id, # room_id
    't': int(time.time() * 1000) # timestamp microsecond
}

"""
import time
from json import loads


class GetLotteryInfo(object):
    """
    获取抽奖信息
    """

    def __init__(self, session):
        self.session = session
        self.default_url = '''https://www.douyu.com/member/lottery/activity_info?t={}&room_id={}'''  # 房间号抽奖信息url
        self.url = ''

    @staticmethod
    def lottery_to_strings(arg):
        # 分析 Lottery_range  得到的数据 抽奖条件
        switcher = {
            0: "",  # Lottery_range = 0
            1: "关注主播、",  # Lottery_range = 1
            2: "加入粉丝团、",  # Lottery_range = 2
            3: "关注主播、加入粉丝团、"  # Lottery_range = 3
        }
        return switcher.get(arg, "nothing")

    def get_lottery_info(self, room_list):
        """
        获取房间抽奖信息
        :param room_list:
        :return:
        """
        lottery_info_list = []
        if room_list:
            for room in room_list:  # 根据房间号获取抽奖信息
                self.url = self.default_url.format(int(time.time() * 1000), room['room_id'])  # 查询url,t参数是时间戳
                response = self.session.get(self.url)
                if response.status_code == 200:
                    if response.text:
                        res_json = loads(response.text)
                        room_id = res_json['data']['room_id']
                        room_name = room['room_name']
                        prize_name = res_json['data']['prize_name']
                        prize_num = res_json['data']['prize_num']
                        start_at = res_json['data']['start_at']  # start time 开始时间，时间戳
                        lottery_range = res_json['data']['join_condition']['lottery_range']
                        lottery_string = self.lottery_to_strings(lottery_range)
                        try:
                            # 有command_content 需要发送口令，没有则不需要，抽奖条件
                            command_content = res_json['data']['join_condition']['command_content']  # join condition
                            if lottery_range == 0:  # lottery_range == 0 时只有一个条件，没有'并'字
                                lottery_string = lottery_string + '发送下方口令'
                            else:
                                lottery_string = lottery_string + '并发送下方口令'
                        except Exception as e:
                            # 有gift_name是需要送礼，没有则不需要，抽奖条件
                            command_content = res_json['data']['join_condition']['gift_name'] + ' X ' + str(
                                res_json['data']['join_condition']['gift_num'])
                            if lottery_range == 0:  # lottery_range == 0 时只有一个条件，没有'并'字
                                lottery_string = lottery_string + '送出下方礼物'
                            else:
                                lottery_string = lottery_string + '并送出下方礼物'
                        lottery_string = lottery_string + '即可参与抽奖'  # 最后加上 '即可参与抽奖'

                        lottery_info = dict()
                        lottery_info['room_id'] = room_id
                        lottery_info['room_name'] = room_name
                        lottery_info['prize_name'] = prize_name
                        lottery_info['prize_num'] = prize_num
                        lottery_info['lottery_range'] = lottery_string
                        lottery_info['start_at'] = (int(start_at) * 1000)
                        lottery_info['command_content'] = command_content
                        lottery_info_list.append(lottery_info)

            return lottery_info_list
        else:
            return None
