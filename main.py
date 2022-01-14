import os
import telebot
import logging
import psycopg2
import requests
from config import *
from flask import Flask, request
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)


response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
print(response.text)


@bot.message_handler(commands=['start'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(commands=['quote'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))

