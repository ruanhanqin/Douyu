from flask import Flask
from flask import render_template
import sqlite3
import os
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_ajax')
def get_ajax():
    sql = '''SELECT * FROM (SELECT * FROM Lottery GROUP BY room_id) AS a GROUP BY 
              start_time ORDER BY start_time DESC LIMIT 50'''  # LIMIT 50
    conn = sqlite3.connect('./Lottery.db')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    lottery_info = []
    for item in result:  # 拼接字典
        i = 0
        info = dict()
        for it in item:
            if i == 0:  # 第一个是ID,不需要
                i += 1
                continue
            if i == 1:
                info['room_id'] = it
            elif i == 2:
                info['room_name'] = it
            elif i == 3:
                info['prize_name'] = it
            elif i == 4:
                info['prize_num'] = it
            elif i == 5:
                info['lottery_range'] = it
            elif i == 6:
                info['start_time'] = it
            elif i == 7:
                info['command_content'] = it
            i += 1
        lottery_info.append(info)

    conn.close()
    return json.dumps(lottery_info)  # 列表转 JSON


@app.route('/get')
def get():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
