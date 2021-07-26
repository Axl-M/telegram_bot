import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

TOKEN = "1875891057:AAFbYy8D7z376OJ-lbx-7AlJ7wWqTXoHXtY"
bot = telegram.Bot(token=TOKEN)
# print(bot.get_me())

updater = Updater(token=TOKEN, use_context=True) # без use_context буде реагировать ТОЛЬКО на последнее сообщение пользователя
dispatcher = updater.dispatcher
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, поговори со мной!')
    print("ok")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'ты написал мне: {update.message.text}')
# updater.start_polling() # запуск бота. Передать start_polling нашему updater-у

# def echo(update, context):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo2)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_cups = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_cups)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def Sasha(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Санёчек любит Анжелику ❤️")

sasha_handler = CommandHandler('Sasha', Sasha)
dispatcher.add_handler(sasha_handler)

def Angelika(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Анжелика любит Сашечку ❤️")

Angelika_handler = CommandHandler('Angelika', Angelika)
dispatcher.add_handler(Angelika_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Такой команды я не знаю :(☹️")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



# перезапусть консоль
# В КОНСОЛИ НАБИРАЕМ
# from t import bot
# from t import updater, dispatcher
# updater.start_polling()
# <queue.Queue object at 0x0131C2E0>
# ПОЛУЧАЕМ ОТКЛИК В ТЕЛЕГРАММ
# ok
