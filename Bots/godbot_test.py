from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Инициализация ботов
bot_molochkov = Bot(token="7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM")  # токен Молочков
bot_gnetusheva = Bot(token="7927595118:AAHM1yefSjBEz972b_xKvHLxRxH5OK_L-os")  # токен Гнетущева

# ID группы
chat_id = -1002411590976  # ID группы

# Локальное хранилище сообщений
message_store = {}

async def store_message(update: Update, context: CallbackContext):
    """
    Сохраняет текст сообщений в локальном хранилище.
    """
    try:
        message = update.message
        if message and message.chat_id == chat_id:
            message_store[message.message_id] = message.text or message.caption or "(Медиа без текста)"
            print(f"[LOG] Сохранено сообщение: ID={message.message_id}, текст='{message_store[message.message_id]}'")
    except Exception as e:
        print(f"[ERROR] Ошибка в store_message: {e}")

async def simulate_reply(update: Update, context: CallbackContext):
    """
    Имитирует ответ, добавляя ссылку на сообщение.
    """
    try:
        if len(context.args) < 3:
            await update.message.reply_text("Ошибка: недостаточно аргументов. Использование: /reply <Молочков|Гнетущева> <ID сообщения> <текст>")
            return

        bot_name = context.args[0]
        try:
            source_message_id = int(context.args[1])
        except ValueError:
            await update.message.reply_text(f"Ошибка: '{context.args[1]}' не является корректным ID сообщения.")
            return

        reply_text = " ".join(context.args[2:])  # Текст ответа

        # Формируем ссылку на сообщение
        link_to_message = f"https://t.me/c/{str(chat_id)[4:]}/{source_message_id}"

        # Извлекаем текст из локального хранилища
        quoted_text = message_store.get(source_message_id, "Текст сообщения недоступен.")

        print(f"[LOG] Попытка ответа на сообщение ID={source_message_id}, текст='{quoted_text}'")

        # Форматируем текст ответа
        formatted_text = (
            f"Ответ на сообщение: [{quoted_text}]({link_to_message})\n\n"
            f"{reply_text}"
        )

        # Отправляем сообщение от выбранного бота
        if bot_name == "Молочков":
            await bot_molochkov.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
            print(f"[LOG] Ответ отправлен ботом Молочков.")
        elif bot_name == "Гнетущева":
            await bot_gnetusheva.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
            print(f"[LOG] Ответ отправлен ботом Гнетущева.")
        else:
            await update.message.reply_text("Неизвестный бот. Используйте Молочков или Гнетущева.")
    except Exception as e:
        print(f"[ERROR] Ошибка в simulate_reply: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

async def log_messages(update: Update, context: CallbackContext):
    """
    Логирует все сообщения, которые бот видит.
    """
    try:
        if update.message and update.message.chat_id == chat_id:
            print(f"[LOG] Сообщение: ID={update.message.message_id}, текст='{update.message.text}'")
    except Exception as e:
        print(f"[ERROR] Ошибка в log_messages: {e}")

async def say_command(update: Update, context: CallbackContext):
    """
    Отправляет сообщение в группу от имени выбранного бота.
    Использование: /say <Молочков|Гнетущева> <текст>
    """
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Ошибка: недостаточно аргументов. Использование: /say <Молочков|Гнетущева> <текст>")
            return

        bot_name = context.args[0]
        message_text = " ".join(context.args[1:])
        print(f"[LOG] Команда /say: Бот={bot_name}, Текст='{message_text}'")

        if bot_name == "Молочков":
            result = await bot_molochkov.send_message(chat_id=chat_id, text=message_text)
            print(f"[LOG] Успешно отправлено ботом Молочков: {result}")
        elif bot_name == "Гнетущева":
            result = await bot_gnetusheva.send_message(chat_id=chat_id, text=message_text)
            print(f"[LOG] Успешно отправлено ботом Гнетущева: {result}")
        else:
            await update.message.reply_text("Неизвестный бот. Используйте Молочков или Гнетущева.")
    except Exception as e:
        print(f"[ERROR] Ошибка в /say: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    TOKEN = "7802864450:AAE1UF3z5OYIXpPK-pstTdEP4wTyHFW4hGM"
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("reply", simulate_reply))
    application.add_handler(CommandHandler("say", say_command))
    application.add_handler(MessageHandler(filters.Chat(chat_id), store_message))
    application.add_handler(MessageHandler(filters.Chat(chat_id), log_messages))

    print("Управляющий бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
