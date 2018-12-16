#!/usr/bin/env python
# -*-encoding: utf-8-*-


import requests
from Douyu import getLotteryInfo, dataBase, getLotteryRoomId
import time


if __name__ == '__main__':
    count = 500
    LotteryInfoLists = []
    session = requests.Session()
    get_room_id = getLotteryRoomId.GetLotteryRoomId(session=session)
    get_lottery_info = getLotteryInfo.GetLotteryInfo(session=session)
    sqlite_conn = dataBase.DataBase()
    while True:
        for i in range(count):
            if i == count - 1:
                time.sleep(300)
                continue
            try:
                room_list = get_room_id.get_room_id(i + 1)
                lottery_info = get_lottery_info.get_lottery_info(room_list)
                sqlite_conn.insert_data(lottery_info)
            except Exception as e:
                print(e)
            finally:
                time.sleep(15)
