from telegram import Bot

# Ваш токен
TOKEN = "7927595118:AAHM1yefSjBEz972b_xKvHLxRxH5OK_L-os"
bot = Bot(token=TOKEN)

# ID чата, куда отправлять сообщение
chat_id = -4755516495

# ID сообщения, на которое бот отвечает
reply_to_message_id = "ID_СООБЩЕНИЯ"

# Текст сообщения, которое вы хотите отправить
message_text = "Спасибо, Леонид Вассильевич!"

# Отправка сообщения
bot.send_message(
    chat_id=chat_id,
    text=message_text,
    reply_to_message_id=reply_to_message_id
)
