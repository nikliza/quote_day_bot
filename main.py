import os
import telebot
import logging
import psycopg2
import requests
from config import *
from flask import Flask, request
from telebot import types


bot = telebot.TeleBot(BOT_TOKEN)


response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
print(response.text)


@bot.message_handler(commands=['start'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(commands=['quote'])
def quote_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)
    makup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text = 'ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')

    makup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Вам понравилась цитата?',
                     reply_markup=makup_inline
                     )

@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    if call.data == 'yes':
        bot.reply_to(call, call.data)
    else:
        bot.reply_to(call, call.data)

bot.polling(none_stop=True)