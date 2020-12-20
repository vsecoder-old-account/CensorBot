# -*- coding: utf-8 -*-

#import telebot

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import re
import datetime
import string
import time
import json
import requests

bot_token = '<token>'
#bot = telebot.TeleBot(bot_token)
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

GROUP_ID = -329119522  # ID моей группы

# считаем для статистики
allwords = 161
matwords = 5
filescan = 15

@dp.message_handler(commands=['help', 'start'])
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    await bot.send_message(message.chat.id, 'Здравствуйте, я бот, который будет удалять маты из чата, '
        'если вы заметили что какой - то мат не удаляется, для того чтобы я начал работать,'
        'просто добавьте меня в чат, зайдите в настройки, и выдайте мне права администратора!')

@dp.message_handler(commands=['info', 'me'])
async def info(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    await bot.send_message(message.chat.id, 'Ну раз спросил, то в мои возможности входят несколько функций, '
        'я обрабатываю все сообщения пользователей, и если это сообщение содержит мат, то я его удаляю, '
        'но на всякий случай я присылаю сообщение помеченное вашим именем, а вместо матов три точки,'
        'из этого я веду статистику, и приветствую новых пользователей!'
        'Так же обрабатываю файлы присылая про них развёрнутую статистику проверки на вирусы для вашей безопасности!')

@dp.message_handler(commands=['static', 'info'])
async def statistic(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    await bot.send_message(
        message.chat.id, '<b>Всего слов обработанно:</b> <code>' + str(allwords) +
        '</code>\n<b>Слов с матами:</b> <code>' + str(matwords) +
        '</code>\n<b>Файлов отсканировано:</b> <code>' + str(filescan) + '</code>', parse_mode='html')

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    await bot.send_message(
        message.chat.id, 'Правила чата: \n'
        '<b> · </b>Не оскорбляйте других участников, не создавайте конфликтных ситуаций. Давайте формировать комьюнити, а не ругаться.'
        '\n<b> · </b>Не используйте нецензурную лексику — сразу удалится ботом.'
        '\n<b> · </b>Мы любим полезные материалы — можете присылать ссылки и делиться ими с другими участниками.'
        '\n<b> · </b>Нельзя рекламировать услуги, товары, складчины, давать ссылки на конкурентные ресурсы и те, которые не относятся к теме вёрстки и программирования.'
        '\n<b> · </b>Если вы хотите написать в чат, старайтесь уместить свою мысль в одно сообщение — никто не любит флуд.'
        '\n<b> · </b>Голосовые сообщения приберегите для друзей — пишите текстом.', parse_mode='html')

@dp.message_handler(content_types=["new_chat_members"])
async def newuser(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    if message.from_user.username is None:
        await bot.send_message(
            message.chat.id, 'Приветствую вас в чате @' + message.new_chat_members.username + ', я <b>бот</b>, и вот <u>правила</u> чата: \n'
            '<b> · </b>Не оскорбляйте других участников, не создавайте конфликтных ситуаций. Давайте формировать комьюнити, а не ругаться.'
            '\n<b> · </b>Не используйте нецензурную лексику — сразу удалится ботом.'
            '\n<b> · </b>Мы любим полезные материалы — можете присылать ссылки и делиться ими с другими участниками.'
            '\n<b> · </b>Нельзя рекламировать услуги, товары, складчины, давать ссылки на конкурентные ресурсы и те, которые не относятся к теме вёрстки и программирования.'
            '\n<b> · </b>Если вы хотите написать в чат, старайтесь уместить свою мысль в одно сообщение — никто не любит флуд.'
            '\n<b> · </b>Голосовые сообщения приберегите для друзей — пишите текстом.', parse_mode='html')
    else:
        await message.reply(
            'Приветствую вас в чате, я <b>бот</b>, и вот <u>правила</u> чата: \n'
            '<b> · </b>Не оскорбляйте других участников, не создавайте конфликтных ситуаций. Давайте формировать комьюнити, а не ругаться.'
            '\n<b> · </b>Не используйте нецензурную лексику — сразу удалится ботом.'
            '\n<b> · </b>Мы любим полезные материалы — можете присылать ссылки и делиться ими с другими участниками.'
            '\n<b> · </b>Нельзя рекламировать услуги, товары, складчины, давать ссылки на конкурентные ресурсы и те, которые не относятся к теме вёрстки и программирования.'
            '\n<b> · </b>Если вы хотите написать в чат, старайтесь уместить свою мысль в одно сообщение — никто не любит флуд.'
            '\n<b> · </b>Голосовые сообщения приберегите для друзей — пишите текстом.', parse_mode='html')

@dp.message_handler(content_types=["left_chat_member"])
async def leftuser(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    await bot.send_message(
        message.chat.id, 'Эх... минус один пользователь чата...', parse_mode='html')

@dp.message_handler(content_types=["text"])
async def check(message: types.Message):
    global allwords, matwords
    try:
        if message.text == '@myCensorBot':
            sti = open('dist/1.tgs', 'rb')
            await bot.send_sticker(message.chat.id, sti)
            await bot.send_message(message.chat.id, 'Я!')
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
                                await bot.delete_message(
                                    message.chat.id, message.message_id)
                                await bot.send_message(
                                    message.chat.id, '🤐 @' + message.from_user.username + '\n' + text)
                                matwords += 1
                            break
                        for word in ntext.split():
                            if word == part:
                                text = text.replace(part, '. . .', 1000)
                                mat = True
        
    except BaseException as e:
        await bot.send_message(message.chat.id, 'Упс, ошибка...\n<code>' + e + '</code>', parse_mode='html')


@dp.message_handler(content_types=['document'])
async def file_handler(message: types.Message):
    global filescan
    try:
        url_file_scan = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = dict(apikey='<api_key>')
        file_upload_id = await bot.get_file(message.document.file_id)
        url_upload_file = "https://api.telegram.org/file/bot{}/{}".format(bot_token, file_upload_id.file_path)
        recvfile = requests.get(url_upload_file)
        files = dict(file=(recvfile.content))
        response_file_scan = requests.post(url_file_scan, files=files, params=params)
        if response_file_scan.json()['response_code'] == 1:
            await bot.send_message(message.chat.id, "<a href='" + response_file_scan.json()['permalink'] + "'>Информация</a> о отправленом файле", parse_mode='html')
        else:
            await bot.send_message(message.chat.id, response_file_scan.json()['verbose_msg'])
        filescan += 1
    except BaseException as e:
        await bot.send_message(message.chat.id, 'Упс, ошибка...\n<code>' + e + '</code>', parse_mode='html')

#
if __name__ == "__main__":
    executor.start_polling(dp)
