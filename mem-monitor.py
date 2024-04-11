import os
import psutil
import requests
import time
from dotenv import load_dotenv

# Загрузка переменных среды из файла .env
load_dotenv()

# URL для отправки HTTP-запроса
url = os.getenv('API_URL', 'http://127.0.0.1:8080')

# Пороговое значение для потребления памяти (в процентах)
threshold = int(os.getenv('MEMORY_THRESHOLD', '20'))

def check_memory_usage():
    # Получаем информацию о потреблении памяти
    memory_percent = psutil.virtual_memory().percent
    return memory_percent

def send_http_request(mem):
    current_utc_time = time.gmtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_utc_time)
    # Отправляем HTTP-запрос
    response = requests.post(url, json={"memory_usage" : mem, "current_time" : formatted_time})
    if response.status_code == 200:
        print("HTTP запрос отправлен успешно")

while True:
    memory_percent = check_memory_usage()
    print("Потребление памяти:", memory_percent)

    if memory_percent > threshold:
        print("Потребление памяти превышает пороговое значение. Отправка HTTP-запроса...")
        try:
            send_http_request(memory_percent)
        except:
            print("При отправке запроса произошла ошибка")
            pass

    # Пауза между проверками (в секундах)
    time.sleep(int(os.getenv('SLEEP_INTERVAL', 60)))  # каждую минуту
