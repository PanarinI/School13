from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Инициализация ботов
bot_molochkov = Bot(token="7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM")
bot_gnetusheva = Bot(token="7927595118:AAHM1yefSjBEz972b_xKvHLxRxH5OK_L-os")

# ID группы
chat_id = -1002411590976   # Укажите реальный chat_id группы

# История сообщений
chat_history = []

async def add_message_to_history(character, text):
    """
    Добавляет сообщение в историю.
    """
    chat_history.append(f"{character}: {text}")
    if len(chat_history) > 20:  # Ограничение истории
        chat_history.pop(0)

async def generate_response(character_name, context):
    """
    Генерация ответа для персонажа (заглушка GPT).
    """
    if character_name == "Молочков":
        return "Давайте обсудим это на следующем собрании."
    elif character_name == "Гнетущева":
        return "Дисциплина — основа всего."
    else:
        return "Интересный вопрос..."

async def chat_simulation(update: Update, context: CallbackContext):
    """
    Имитирует общение между персонажами.
    """
    user_message = " ".join(context.args)
    if not user_message:
        await update.message.reply_text("Ошибка: сообщение не указано.")
        return

    # Сохраняем сообщение пользователя
    await add_message_to_history("Пользователь", user_message)

    # Генерация и отправка ответов от персонажей
    for character, bot in [("Молочков", bot_molochkov), ("Гнетущева", bot_gnetusheva)]:
        # Генерация ответа
        context_text = "\n".join(chat_history)
        reply = await generate_response(character, context_text)

        # Сохраняем ответ в историю
        await add_message_to_history(character, reply)

        # Отправляем сообщение от имени персонажа
        try:
            await bot.send_message(chat_id=chat_id, text=reply)
        except Exception as e:
            print(f"Ошибка отправки от {character}: {e}")

def main():
    TOKEN = "7802864450:AAE1UF3z5OYIXpPK-pstTdEP4wTyHFW4hGM"
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("simulate", chat_simulation))

    print("Управляющий бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
