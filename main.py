import os
import telebot
import logging
import psycopg2
import requests
from config import *
from flask import Flask, request
from telebot import types


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
print(response.text)


@bot.message_handler(commands=['start'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)



