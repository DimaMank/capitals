import telebot
import config
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])  # Запускаем бот
def welcome_start(message):
    bot.send_message(message.chat.id, 'Чтобы узнать столицу страны введи ее название')

@bot.message_handler(content_types='text')
def capital(message):
    countries = {}
    url = 'http://ostranah.ru/_lists/capitals.php'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    table = soup.find('table', {'class': 'type-list short-list'})
    tr = table.find_all('td')
    lista = []
    for a in tr:
        lista.append(a.text.strip(' ').lower())
    for i in range(len(lista)):
        if i == 0 or i % 2 == 0:
            countries[lista[i]] = lista[i + 1]
    demand = message.text.lower()
    try:
        cap = countries.get(demand).capitalize()
        bot.send_message(message.chat.id, cap)
    except:
        bot.send_message(message.chat.id, 'Такой страны нет')

bot.polling()  # запускаем бота