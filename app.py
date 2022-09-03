from flask import Flask
from flask import request as flask_request
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from src.database import Database

app = Flask(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def tg_send_item(chat_id, text):
    """Sends item to telegram"""
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def parse_top_item():
    """Parse required features from db top item"""
    db = Database()

    top_flat_link = db.get_top_item()
    link = top_flat_link.link
    price = top_flat_link.price
    subway = top_flat_link.subway
    item_id = top_flat_link.item_id

    db.update_shown_item(item_id)  # Set DB.shown = 1 for sent item

    return link, price, subway, item_id


@app.route("/", methods=["POST"])
def main():
    """Send listing to telegram"""
    link, price, subway, _ = parse_top_item()

    chat_id = flask_request.json["message"]["chat"]["id"]
    tg_send_item(chat_id=chat_id, text=f"test")
    tg_send_item(chat_id=chat_id, text=f"Цена {price}")
    tg_send_item(chat_id=chat_id, text=f"Метро {subway}")
    tg_send_item(chat_id=chat_id, text=f"{link}")

    return {"ok": True}


if __name__ == "__main__":
    #app.run()
    app.run(port=5000, host='0.0.0.0')
