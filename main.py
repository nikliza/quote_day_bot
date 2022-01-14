import requests
import telebot
bot = telebot.TeleBot("5025840937:AAETRY14UP2PPgmf3v_MUW8KxSup2An_CUA")

response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
print(response.text)

@bot.message_handler(commands=['start'])
def start_message(message):
    response = requests.get('http://api.forismatic.com/api/1.0/?method=getQuote&format=text')
    bot.send_message(message.chat.id, response.text)