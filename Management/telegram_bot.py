
##код для публикации сообщения

from telegram import Update
from telegram.ext import Updater, CommandHandler

# Токен вашего бота
TOKEN = "7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM"

# Функция для команды /start
def start(update, context):
    update.message.reply_text(
        "Добро пожаловать! Я директор Молочков. Чем могу помочь?"
    )

# Функция для публикации сообщения
def post_message(update, context):
    update.message.reply_text("Порядок — основа всего. Соблюдайте его!")

# Настройка бота
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# Добавляем команды
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("post", post_message))

# Запуск бота
updater.start_polling()
updater.idle()
