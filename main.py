import os
import telebot
import logging
import psycopg2
import requests
from config import *
from flask import Flask, request
from telebot import types

db_connection = psycopg2.connect(
    host =HOST,
    user = User,
    password = Password,
    database = Database
)
db_object = db_connection.cursor()

bot = telebot.TeleBot(TOKEN)

def update_messages_count(user_id):
    db_connection = psycopg2.connect(DB_URI, sslmode="require")
    db_object = db_connection.cursor()
    db_object.execute(f"UPDATE users SET messages = messages + 1 WHERE id = {user_id}")
    db_connection.commit()


@bot.message_handler(commands=["start"])
def start(message):
    def quote_message(message):
        response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
        bot.send_message(message.chat.id, response.text)

    user_id = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")
    db_connection = psycopg2.connect(DB_URI, sslmode="require")
    db_object = db_connection.cursor()
    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()

    update_messages_count(user_id)


bot.polling()