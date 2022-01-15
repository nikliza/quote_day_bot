import os
from telebot import types
import requests
from flask import Flask, request
from config import *
import telebot


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


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

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route(f"/{TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))