import json
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import os



# Загрузить стоп-слова для фильтрации
nltk.download('punkt')
nltk.download('stopwords')

# Замените 'group_chat.json' на путь к вашему JSON-файлу
file_path = 'F:/PythonProject/School13/Ref/alit.json'

if not os.path.exists(file_path):
    print(f"Файл не найден: {file_path}")
    exit(1)

# Функция для извлечения текстовых сообщений из JSON
# Функция для извлечения текстовых сообщений из JSON
def extract_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        messages = []
        for message in data.get('messages', []):
            text_content = message.get('text', [])

            # Если текст является списком (как в вашем примере)
            if isinstance(text_content, list):
                combined_text = ""
                for item in text_content:
                    if isinstance(item, str):  # Если элемент - строка
                        combined_text += item
                    elif isinstance(item, dict) and 'text' in item:  # Если элемент - объект с ключом "text"
                        combined_text += item['text']
                messages.append(combined_text)

            # Если текст - строка (редкий случай в вашей структуре)
            elif isinstance(text_content, str):
                messages.append(text_content)
        return messages


# Функция для обработки текста и подсчета частот ключевых слов
def analyze_keywords(messages, top_n=30):
    stop_words = set(stopwords.words('russian') + stopwords.words('english'))
    all_words = []

    for message in messages:
        if isinstance(message, str):  # Обрабатываем только строковые сообщения
            words = word_tokenize(message.lower())
            filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
            all_words.extend(filtered_words)

    word_freq = Counter(all_words)
    return word_freq.most_common(top_n)

# Основная часть
if __name__ == "__main__":
    messages = extract_messages(file_path)
    top_keywords = analyze_keywords(messages)

    print("Топ ключевых слов:")
    for keyword, freq in top_keywords:
        print(f"{keyword}: {freq}")

print(os.getcwd())



