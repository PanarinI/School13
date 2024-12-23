import asyncio
from telegram import Bot

# Токен вашего бота
TOKEN = "7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM"

# ID вашей группы
GROUP_ID = -4755516495  # Укажите ID вашей группы

# Асинхронная функция для отправки сообщения
async def send_message_to_group():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=GROUP_ID, text="Добро пожаловать в Школу имени Послушного!")

# Запускаем асинхронную функцию
if __name__ == "__main__":
    asyncio.run(send_message_to_group())


# python Bots\new_message.py
