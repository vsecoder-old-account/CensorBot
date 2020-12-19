# -*- coding: utf-8 -*-

import telebot
import re
import datetime
import string
import time
import json
import requests

bot_token = '<token>'
bot = telebot.TeleBot(bot_token)

GROUP_ID = -329119522  # ID моей группы

# считаем для статистики
allwords = 161
matwords = 5
filescan = 15

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    bot.send_message(message.chat.id, 'Здравствуйте, я бот, который будет удалять маты из чата, если вы заметили что какой-то мат не удаляется, для того чтобы я начал работать, просто добавьте меня в чат, зайдите в настройки, и выдайте мне права администратора!')

@bot.message_handler(commands=['static', 'info'])
def statistic(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    bot.send_message(
        message.chat.id, '<b>Всего слов обработанно:</b> <code>' + str(allwords) +
        '</code>\n<b>Слов с матами:</b> <code>' + str(matwords) +
        '</code>\n<b>Файлов отсканировано:</b> <code>' + str(filescan) + '</code>', parse_mode='html')

@bot.message_handler(commands=['rules'])
def rules(message):
    bot.send_message(
        message.chat.id, 'Правила чата: \n'
        '<b> · </b>Не оскорбляйте других участников, не создавайте конфликтных ситуаций. Давайте формировать комьюнити, а не ругаться.'
        '\n<b> · </b>Не используйте нецензурную лексику — сразу удалится ботом.'
        '\n<b> · </b>Мы любим полезные материалы — можете присылать ссылки и делиться ими с другими участниками.'
        '\n<b> · </b>Нельзя рекламировать услуги, товары, складчины, давать ссылки на конкурентные ресурсы и те, которые не относятся к теме вёрстки и программирования.'
        '\n<b> · </b>Если вы хотите написать в чат, старайтесь уместить свою мысль в одно сообщение — никто не любит флуд.'
        '\n<b> · </b>Голосовые сообщения приберегите для друзей — пишите текстом.', parse_mode='html')

@bot.message_handler(content_types=["new_chat_members"])
def newuser(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    bot.send_message(
        message.chat.id, 'Приветствую вас в чате @' + message.new_chat_member.username + ', я <b>бот</b>, и вот <u>правила</u> чата: \n'
        '<b> · </b>Не оскорбляйте других участников, не создавайте конфликтных ситуаций. Давайте формировать комьюнити, а не ругаться.'
        '\n<b> · </b>Не используйте нецензурную лексику — сразу удалится ботом.'
        '\n<b> · </b>Мы любим полезные материалы — можете присылать ссылки и делиться ими с другими участниками.'
        '\n<b> · </b>Нельзя рекламировать услуги, товары, складчины, давать ссылки на конкурентные ресурсы и те, которые не относятся к теме вёрстки и программирования.'
        '\n<b> · </b>Если вы хотите написать в чат, старайтесь уместить свою мысль в одно сообщение — никто не любит флуд.'
        '\n<b> · </b>Голосовые сообщения приберегите для друзей — пишите текстом.', parse_mode='html')


@bot.message_handler(func=lambda message: message.text and message.text.lower())
def check(message):
    global allwords, matwords
    if message.text == '@myCensorBot':
        sti = open('dist/1.tgs', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id, 'Я!')
    else:
        with open("dist/mats.txt", encoding='utf-8') as openfile:
            mat = False
            text = message.text.lower()
            ntext = text.translate(str.maketrans('', '', string.punctuation)).lower()
            allwords += 1
            for line in openfile:
                mat = False
                for part in line.split():
                    part = part.rstrip(',')
                    if part == 'endmats':
                        if mat == True:
                            bot.delete_message(
                                message.chat.id, message.message_id)
                            bot.send_message(
                                message.chat.id, '🤐 @' + message.from_user.username + '\n' + text)
                            matwords += 1
                        break
                    for word in ntext.split():
                        if word == part:
                            text = text.replace(part, '. . .', 1000)
                            mat = True


@bot.message_handler(content_types=['document'])
def file_handler(message):
    global filescan
    url_file_scan = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = dict(apikey='<api_key>')
    file_upload_id = bot.get_file(message.document.file_id)
    url_upload_file = "https://api.telegram.org/file/bot{}/{}".format(bot_token, file_upload_id.file_path)
    recvfile = requests.get(url_upload_file)
    files = dict(file=(recvfile.content))
    response_file_scan = requests.post(url_file_scan, files=files, params=params)
    if response_file_scan.json()['response_code'] == 1:
        bot.send_message(message.chat.id, "<a href='" + response_file_scan.json()['permalink'] + "'>Информация</a> с virustotal о отправленом файле", parse_mode='html')
    else:
        bot.send_message(
            message.chat.id, response_file_scan.json()['verbose_msg'])
    filescan += 1

#
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
