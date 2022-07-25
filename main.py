from flask import Flask, request
import json
import os
from os.path import join, dirname
import requests
import dotenv
from dotenv import load_dotenv


app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращает токен


def send_flats(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route("/", methods=["POST"])
def main():
    chat_id = request.json["message"]["chat"]["id"]
    send_flats(chat_id=chat_id, text="msg")
    return {"ok": True}


if __name__ == "__main__":
    # get top-1 card sorted by rating from db
    # sended items marks 'shown'
    # 'where name != 'showm'

    app.run()
