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



response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
print(response.text)


@bot.message_handler(commands=['start'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(commands=['quote'])
def quote_command(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)
    makeup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')

    makeup_inline.add(item_yes,item_no)
    bot.send_message(message.chat.id, 'Вам нравится эта цитата?',
                     reply_markup= makeup_inline
                     )

def answer(call):
    if call.data == 'yes':
        pass
    else:
        pass