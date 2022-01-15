import os

from flask import Flask, request
from config import *
import telebot


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello')


bot.polling()

