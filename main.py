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
        makoup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_live = types.KeyboardButton('Жизнь')
        item_l0ve = types.KeyboardButton('Любовь')

        makoup_reply.add(item_live, item_l0ve)
        bot.send_message(call.message.chat.id, 'Какая у цитаты тема?',
                         reply_markup=makoup_reply)
    else:
        answer = 'no'
    bot.send_message(call.message.chat.id, answer)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Жизнь':
        bot.send_message(message.chat.id, 'жизнь')
    else:
        bot.send_message(message.chat.id, 'любовь')


@bot.message_handler(commands=['quota'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
    bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?", reply_markup=markup)


bot.polling(none_stop=True)