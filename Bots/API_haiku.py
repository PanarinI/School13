

import openai

openai.api_key = "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"

try:
    response = openai.Model.list()
    print("Модели доступны:", [model["id"] for model in response["data"]])
except openai.error.OpenAIError as e:
    print(f"Ошибка: {e}")
