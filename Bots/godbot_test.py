import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Инициализация ботов
bots = {
    "Молочков": Bot(token="7631144398:AAH0wlvD3Q-8pk1lBqcTPoQ7iGHiqBL0XBM"),
    "Гнетущева": Bot(token="7927595118:AAHM1yefSjBEz972b_xKvHLxRxH5OK_L-os"),
    "Кривобук": Bot(token="7740299507:AAEhmKmcmGJABXDkOzL7be2O7FVARoHQYr0"),
    "Щупальцев": Bot(token="7563174810:AAHagFGV1gW3Oa3tEIhbLprRJecQwARz0as"),
    "Недосказов": Bot(token="7201540325:AAGrXrEAwkfOgvsuP5C-uwcLoPv2x1C9B7U"),
    "Укрощённая": Bot(token="7786826547:AAGTpRHddP8CLilEV9bSNcp_mLykedoYr2w"),
    "Смелова": Bot(token="8199998433:AAE37KxE0F_r8LqIwUUzGRIp5Guth76PHUo"),
    "Берёзкин": Bot(token="7903493626:AAHezFJ3bZCC4CLykUJXZyEvQeMrkIEEuNI"),
    "Берёзкина": Bot(token="7165357588:AAGQb1bD8gs504er2zwNQifaXvnE_hFTsQk"),
}

# ID канала и группы обсуждений
channel_id = -1002325502814  # ID вашего канала
discussion_group_id = -1002411590976  # ID группы обсуждений

# Функция обработки сообщений в группе обсуждений
async def handle_discussion_message(update: Update, context: CallbackContext):
    try:
        message = update.message
        logging.info(f"Получено сообщение: ID={message.message_id}, текст={message.text}")
    except Exception as e:
        logging.error(f"Ошибка в обработке сообщения из группы обсуждений: {e}")

# Публикация поста в канале
async def post_to_channel(update: Update, context: CallbackContext):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("Ошибка: недостаточно аргументов. Использование: /post <ТекстСообщения>")
            return

        message_text = " ".join(context.args)
        bot = context.bot

        # Публикуем сообщение в канале
        channel_message = await bot.send_message(chat_id=channel_id, text=message_text)
        logging.info(f"Сообщение опубликовано в канале: ID={channel_message.message_id}")
        await update.message.reply_text(f"Сообщение опубликовано в канале: ID={channel_message.message_id}")
    except Exception as e:
        logging.error(f"Ошибка в /post: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Добавление комментария к посту
async def comment_to_post(update: Update, context: CallbackContext):
    try:
        if len(context.args) < 3:
            await update.message.reply_text("Ошибка: недостаточно аргументов. Использование: /comment <ИмяБота> <IDСообщения> <Текст>")
            return

        bot_name = context.args[0]
        original_message_id = int(context.args[1])
        comment_text = " ".join(context.args[2:])

        bot = bots.get(bot_name)
        if not bot:
            await update.message.reply_text("Ошибка: Неизвестный бот.")
            return

        # Отправляем комментарий
        comment_message = await bot.send_message(
            chat_id=discussion_group_id,
            text=comment_text,
            reply_to_message_id=original_message_id,
        )
        logging.info(f"Комментарий опубликован: ID={comment_message.message_id}")
        await update.message.reply_text(f"Комментарий отправлен: ID={comment_message.message_id}")
    except Exception as e:
        logging.error(f"Ошибка в /comment: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Ответ на сообщение
async def simulate_reply(update: Update, context: CallbackContext):
    """
    Имитирует ответ с ссылкой на сообщение.
    Использование: /reply <ИмяБота> <IDСообщенияВГруппе> <Текст>
    """
    try:
        if len(context.args) < 3:
            await update.message.reply_text(
                "Ошибка: недостаточно аргументов. Использование: /reply <ИмяБота> <IDСообщенияВГруппе> <Текст>"
            )
            return

        bot_name = context.args[0]
        reply_to_message_id = int(context.args[1])  # ID сообщения в группе обсуждений
        reply_text = " ".join(context.args[2:])

        bot = bots.get(bot_name)
        if not bot:
            await update.message.reply_text("Ошибка: Неизвестный бот.")
            return

        # Формируем ссылку на сообщение
        link_to_message = f"https://t.me/c/{str(discussion_group_id)[4:]}/{reply_to_message_id}"

        # Форматируем текст с ссылкой
        formatted_text = (
            f"Ответ на сообщение: [Посмотреть сообщение]({link_to_message})\n\n{reply_text}"
        )

        # Отправляем имитацию ответа
        reply_message = await bot.send_message(
            chat_id=discussion_group_id,
            text=formatted_text,
            parse_mode="Markdown",
        )
        logging.info(f"Имитация ответа отправлена: ID={reply_message.message_id}")
        await update.message.reply_text(f"Ответ отправлен: ID={reply_message.message_id}")
    except Exception as e:
        logging.error(f"Ошибка в /reply: {e}")
        await update.message.reply_text(f"Ошибка: {e}")


# Основная функция
def main():
    TOKEN = "7802864450:AAE1UF3z5OYIXpPK-pstTdEP4wTyHFW4hGM"
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("post", post_to_channel))
    application.add_handler(CommandHandler("comment", comment_to_post))
    application.add_handler(MessageHandler(filters.Chat(discussion_group_id), handle_discussion_message))
    application.add_handler(CommandHandler("reply", simulate_reply))

    logging.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
