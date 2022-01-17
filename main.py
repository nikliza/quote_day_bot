import os
import telebot
import psycopg2
import requests
from config import *
from flask import Flask, request
from telebot import types

db_connection = psycopg2.connect(
    host=HOST,
    user=User,
    password=Password,
    database=Database
)

bot = telebot.TeleBot(TOKEN)


def quota_text():
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    return response.text


def quota_id(quota):
    db_object = db_connection.cursor()
    db_object.execute(f"SELECT id FROM quotas WHERE quota = '{quota}'")
    result = db_object.fetchone()
    return result


last_quota = quota_text()

makup_inline1 = types.InlineKeyboardMarkup()
item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
makup_inline1.add(item_yes, item_no)

makup_inline2 = types.InlineKeyboardMarkup()
item_good = types.InlineKeyboardButton(text='ХОРОШЕЕ', callback_data='good')
item_bad = types.InlineKeyboardButton(text='ПЛОХОЕ', callback_data='bad')
makup_inline2.add(item_good, item_bad)

makup_inline3 = types.InlineKeyboardMarkup()
item_love = types.InlineKeyboardButton(text='ЛЮБОВЬ', callback_data='love')
item_success = types.InlineKeyboardButton(text='УСПЕХ', callback_data='success')
item_other = types.InlineKeyboardButton(text='ДРУГОЕ', callback_data='other')
makup_inline3.add(item_love, item_success, item_other)

makup_inline4 = types.InlineKeyboardMarkup()
item_good = types.InlineKeyboardButton(text='ХОРОШЕЕ', callback_data='good_select')
item_bad = types.InlineKeyboardButton(text='ПЛОХОЕ', callback_data='bad_select')
makup_inline4.add(item_good, item_bad)

makup_inline5 = types.InlineKeyboardMarkup()
item_love = types.InlineKeyboardButton(text='ЛЮБОВЬ', callback_data='love_select')
item_success = types.InlineKeyboardButton(text='УСПЕХ', callback_data='success_select')
item_other = types.InlineKeyboardButton(text='ДРУГОЕ', callback_data='other_select')
makup_inline5.add(item_love, item_success, item_other)


@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    chat_id = call.message.chat.id
    answer = ''
    id = quota_id(last_quota)
    user_id = call.from_user.id
    db_object = db_connection.cursor()

    if call.data == 'yes':
        db_object.execute(f"UPDATE users SET likes = likes + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET likes = likes + 1 WHERE id = {id[0]}")
        db_connection.commit()

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id, "Как настроение вызывает у вас эта цитата?", reply_markup=makup_inline2)


    if call.data == 'no':
        answer = 'эх'
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'good':
        db_object.execute(f"UPDATE users SET good = good + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET good_mood = good_mood + 1 WHERE id = {id[0]}")
        db_connection.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id, "На какую тему данная цитата?", reply_markup=makup_inline3)

    if call.data == 'bad':
        db_object.execute(f"UPDATE users SET bad = bad + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET bad_mood = bad_mood + 1 WHERE id = {id[0]}")
        db_connection.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id, "На какую тему данная цитата?", reply_markup=makup_inline3)

    if call.data == 'love':
        answer = 'Спасибо за ваши ответы'
        db_object.execute(f"UPDATE users SET love = love + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET topic_love = topic_love + 1 WHERE id = {id[0]}")
        db_connection.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'success':
        answer = 'Спасибо за ваши ответы'
        db_object.execute(f"UPDATE users SET success = success + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET topic_success = topic_success + 1 WHERE id = {id[0]}")
        db_connection.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'other':
        answer = 'Спасибо за ваши ответы'
        db_object.execute(f"UPDATE users SET other = other + 1 WHERE id = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE quotas SET topic_other = topic_other + 1 WHERE id = {id[0]}")
        db_connection.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'good_select':
        global s
        s = 'good'
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id, "Выберите тему", reply_markup=makup_inline5)


    if call.data == 'bad_select':
        s = 'bad'
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id, "Выберите тему", reply_markup=makup_inline5)

    if call.data == 'love_select':
        db_object = db_connection.cursor()
        if s == 'good':
            db_object.execute("SELECT quota FROM quotas ORDER BY good_mood, topic_love DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        else:
            db_object.execute("SELECT quota FROM quotas ORDER BY bad_mood, topic_love DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'success_select':
        if s == 'good':
            db_object.execute("SELECT quota FROM quotas ORDER BY good_mood, topic_love DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        else:
            db_object.execute("SELECT quota FROM quotas ORDER BY bad_mood, topic_love DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'other_select':
        if s == 'good':
            db_object.execute("SELECT quota FROM quotas ORDER BY good_mood, topic_other DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        else:
            db_object.execute("SELECT quota FROM quotas ORDER BY bad_mood, topic_other DESC LIMIT 1")
            answer = db_object.fetchall()[0][0]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if len(answer):
        bot.send_message(call.message.chat.id, answer)




@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/stat")
    btn2 = types.KeyboardButton("/quota")
    btn3 = types.KeyboardButton("/select")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Команды: \n\n /quota - новая цитата \n\n /stat - статистика \n\n /select - подбор цитаты', reply_markup=markup)

@bot.message_handler(commands=["stat"])
def start(message):
    db_object = db_connection.cursor()

    db_object.execute("SELECT quota FROM quotas ORDER BY likes DESC LIMIT 3")
    result = db_object.fetchall()

    if result:
        reply_message = "Больше всего лайков набрали цитаты:\n\n"
        for i in result:
            reply_message = reply_message + i[0] +'\n' + '\n'
        bot.reply_to(message, reply_message)

    user_id = message.from_user.id
    db_object.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = db_object.fetchall()
    if not result:
        reply_message = "Вам понравилось 0 цитат\n\n"
    else:
        reply_message = "Вам понравилось " + str(result[0][1]) + ' цитат\n\n'
        if result[0][2] == result[0][3]:
            reply_message += 'Хорошее и плохое настроение было выброно одинаковое колличество раз\n\n'
        elif result[0][2] > result[0][3]:
            reply_message += 'Чаще было выбрано хорошее настроние\n\n'
        else:
            reply_message += 'Чаще было выбрано плохое настроние\n\n'

        topics = [result[0][4], result[0][5], result[0][6]]
        topics_words = ['любовь', 'успех', 'другое']

        popular_topic = (topics.index(max(topics)))

        if max(topics) == 0:
            reply_message += 'Вы ни разу не выбирали тему'
        else:
            reply_message += 'Самая популярная тема: ' + topics_words[popular_topic]

    bot.reply_to(message, reply_message)


@bot.message_handler(commands=["quota"])
def quota(message):

    db_object = db_connection.cursor()
    user_id = message.from_user.id
    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO users(id) VALUES ('{user_id}')")
        db_connection.commit()
    bot.send_message(message.chat.id, last_quota)

    result = quota_id(last_quota)
    if not result:
        db_object.execute(f"INSERT INTO quotas(quota) VALUES ('{last_quota}')")
        db_connection.commit()


    bot.send_message(message.chat.id, 'Вам понравилась цитата?',
                     reply_markup=makup_inline1
                     )

@bot.message_handler(commands=["select"])
def select(message):
    bot.send_message(message.chat.id, 'Выберите настроение?',
                     reply_markup=makup_inline4
                     )
bot.polling()
