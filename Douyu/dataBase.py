#!/usr/bin/env python
# -*-encoding: utf-8-*-

"""
DataBase Utils
先执行schema.sql 创建数据库
"""

import sqlite3


class DataBase(object):
    def __init__(self):
        self.insert_sql = '''INSERT INTO lOTTERY(ROOM_ID,ROOM_NAME,PRIZE_NAME,PRIZE_NUM,LOTTERY_RANGE,START_TIME,COMMAND_CONTENT) SELECT 
              '{}','{}','{}','{}','{}',{},'{}' WHERE NOT EXISTS (SELECT ROOM_ID ,START_TIME FROM lOTTERY WHERE ROOM_ID='{}'AND START_TIME={})'''
        self.query_sql = '''SELECT * FROM lOTTERY'''
        self.conn = None

    def connect_db(self):
        conn = sqlite3.connect('./Lottery.db')
        self.conn = conn

    def insert_data(self, lottery_info_list):
        if lottery_info_list:
            self.connect_db()
            cursors = self.conn.cursor()
            for item in lottery_info_list:
                _time = int(item['start_at']) / 1000
                unix_time = ("(datetime(%d,'unixepoch','localtime'))" % _time)  # 转成unix时间
                sql = self.insert_sql.format(item['room_id'], item['room_name'], item['prize_name'], item['prize_num'],
                                             item['lottery_range'], unix_time, item['command_content'], item['room_id'],
                                             unix_time)

                cursors.execute(sql)
                self.conn.commit()
            self.conn.close()

    def query_data(self):
        cursors = self.conn.cursor()
        cursors.execute(self.query_sql)
        ret = cursors.fetchall()
