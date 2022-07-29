from turtle import delay
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import telebot

token = '5364507190:AAFF4cZBqsSNf7Bos9HscDmRt0xS-XoIm4Q'


def get_data(x):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    data = requests.get('https://www.rbc.ua/ukr', headers=headers)
    soup = BeautifulSoup(data.text, "lxml")
    news = soup.find_all(class_='item')

    c = []
    for i in news:

        for j in i.text.split(' '):

            if x in j.lower():

                c.append(i)

    return (c)


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(
            message.chat.id, "Введіть слово чи частину слова для пошуку новин в стрічці сайту РБК.")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        x = message.text.lower()
        try:
            req = get_data(x)
            print(len(req))

            if len(req) == 0:
                bot.send_message(
                    message.chat.id, "За  данним запитом новин немає")
            for i in range(len(req)):
                bot.send_message(
                    message.chat.id, req[i].text)
                delay(1000)

        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Damn...Something was wrong...")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
