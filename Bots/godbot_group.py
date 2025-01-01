from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes

# Инициализация ботов
bot_molochkov = Bot(token="7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM")  # токен Молочков
bot_gnetusheva = Bot(token="7927595118:AAHM1yefSjBEz972b_xKvHLxRxH5OK_L-os")  # токен Гнетущева
bot_krivobuk_math = Bot(token="7740299507:AAEhmKmcmGJABXDkOzL7be2O7FVARoHQYr0")
bot_nedoskazov_english = Bot(token="7201540325:AAGrXrEAwkfOgvsuP5C-uwcLoPv2x1C9B7U")
bot_schupaltsev_bio = Bot(token="7563174810:AAHagFGV1gW3Oa3tEIhbLprRJecQwARz0as")
bot_ukroschennaya_psy = Bot(token="7786826547:AAGTpRHddP8CLilEV9bSNcp_mLykedoYr2w")
bot_smelovaM = Bot(token="8199998433:AAE37KxE0F_r8LqIwUUzGRIp5Guth76PHUo")
bot_berezkinV = Bot(token="7903493626:AAHezFJ3bZCC4CLykUJXZyEvQeMrkIEEuNI")
bot_berezkinaEV = Bot(token="7165357588:AAGQb1bD8gs504er2zwNQifaXvnE_hFTsQk")

# ID группы
chat_id = -1002411590976  # ID группы

# Функция для гибридной имитации ответа
async def simulate_reply(update: Update, context: CallbackContext):
    """
    Имитирует ответ, добавляя ссылку на сообщение и цитату начала сообщения.
    Использование: /reply <Молочков|Гнетущева> <ID сообщения> <текст ответа>
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

        # Попытка получить текст сообщения
        quoted_text = "(Не удалось получить текст сообщения)"
        try:
            async for message in bot_molochkov.get_chat(chat_id).get_history(limit=100):  # Загружаем до 100 сообщений
                if message.message_id == source_message_id:
                    if message.text:
                        quoted_text = message.text[:50]  # Берём первые 50 символов текста
                    elif message.caption:
                        quoted_text = message.caption[:50]  # Берём первые 50 символов подписи к медиа
                    else:
                        quoted_text = "(Сообщение содержит медиа без текста)"
                    break
        except Exception as e:
            print(f"Ошибка при получении истории сообщений: {e}")


        # Форматируем текст ответа
        formatted_text = (
            f"Ответ на сообщение: [Перейти к сообщению]({link_to_message})\n"
            f"{reply_text}"
        )

        # Отправляем сообщение от выбранного бота
        if bot_name == "Молочков":
            await bot_molochkov.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Гнетущева":
            await bot_gnetusheva.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Кривобук":
            await bot_krivobuk_math.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Щупальцев":
            await bot_schupaltsev_bio.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Недосказов":
            await bot_nedoskazov_english.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Укрощённая":
            await bot_ukroschennaya_psy.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Смелова":
            await bot_smelovaM.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Берёзкин":
            await bot_berezkinV.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        elif bot_name == "Берёзкина":
            await bot_berezkinaEV.send_message(chat_id=chat_id, text=formatted_text, parse_mode="Markdown")
        else:
            await update.message.reply_text("Неизвестный бот.")
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Логирование сообщений группы
async def log_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        print(f"Сообщение: ID={update.message.message_id}, текст='{update.message.text}'")
    else:
        print("Получено событие без сообщения.")


# Функция для отправки сообщений
async def say_command(update: Update, context: CallbackContext):
    """
    Отправляет сообщение в группу от имени выбранного бота.
    Использование: /say <Молочков|Гнетущева> <текст>
    """
    try:
        bot_name = context.args[0]  # Имя бота
        message_text = " ".join(context.args[1:])  # Текст сообщения
        print(f"Команда /say: Бот={bot_name}, Текст='{message_text}'")

        if bot_name == "Молочков":
            result = await bot_molochkov.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Гнетущева":
            result = await bot_gnetusheva.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Кривобук":
            result = await bot_krivobuk_math.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Щупальцев":
            result = await bot_schupaltsev_bio.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Недосказов":
            result = await bot_nedoskazov_english.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Укрощённая":
            result = await bot_ukroschennaya_psy.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Смелова":
            result = await bot_smelovaM.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Берёзкин":
            result = await bot_berezkinV.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        elif bot_name == "Берёзкина":
            result = await bot_berezkinaEV.send_message(chat_id=chat_id, text=message_text)
            print(f"Успешно отправлено: {result}")
        else:
            await update.message.reply_text("Неизвестный бот. а.")
    except Exception as e:
        print(f"Ошибка в /say: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Основная функция
def main():
    # Токен управляющего бота
    TOKEN = "7802864450:AAE1UF3z5OYIXpPK-pstTdEP4wTyHFW4hGM"
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("reply", simulate_reply))  # Имитируем ответ
    application.add_handler(CommandHandler("say", say_command))  # Отправка сообщений
    application.add_handler(MessageHandler(filters.Chat(chat_id), log_messages))  # Логирование сообщений

    print("Управляющий бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
