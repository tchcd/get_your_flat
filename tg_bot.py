# В боте по кнопке еще отправялем топ-5 объявлений
# Те, который отправили больше не отправляем
# Помечаем отправленные в БД 'sended' и исключаем их из отправки 'when name != 'sended'
# limit 5
#
# sql = '''
# SELECT t.link FROM table t
# ORDER BY t.evaluation DESC
# LIMIT 5
# '''


# Тут логика бота
from flask import Flask, request
import json
import os
from os.path import join, dirname
import requests
import dotenv
from dotenv import load_dotenv

app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращает токен


def send_flats(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


#
# def calc_sum(nums):
#     res = 0
#     for n in nums:
#         res += n
#     return res


@app.route('/', methods=["POST"])
def hello():
    chat_id = request.json['message']['chat']['id']
    send_flats(chat_id=chat_id, text='Передал')
    return {'ok': True}


# @app.route('/sum')
# def sum_handler():
#     if request.method == "POST":
#         data = request.get_json(force=True)
#         numbers = data['numbers']
#
#         result = calc_sum(numbers)
#
#         response = {'result': result}
#         return json.dumps(response)
#     else:
#         return 'Use POST query!'
#

if __name__ == '__main__':
    app.run()
