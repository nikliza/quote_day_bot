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
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(commands=['s'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)