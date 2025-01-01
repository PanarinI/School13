import asyncio
from telegram import Bot


async def get_channel_id():
    bot_token = "7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM"  # Замените на токен вашего бота
    bot = Bot(token=bot_token)
    updates = await bot.get_updates()

    for update in updates:
        if update.channel_post:
            print(f"ID канала: {update.channel_post.chat.id}")


# Запускаем асинхронную функцию
asyncio.run(get_channel_id())
