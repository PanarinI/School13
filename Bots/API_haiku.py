from dotenv import load_dotenv
import openai
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем ключ из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.Model.list()
    print("Модели доступны:", [model["id"] for model in response["data"]])
except openai.error.OpenAIError as e:
    print(f"Ошибка: {e}")
