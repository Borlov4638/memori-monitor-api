#!/bin/bash

# Загрузка переменных среды из файла .env
source .env

while true; do
    # Получаем текущее использование памяти
    MEMORY_USAGE=$(free | awk '/^Mem:/{print ($3/$2)*100}')

    # Округляем значение использования памяти до целого числа
    MEMORY_USAGE=${MEMORY_USAGE%.*}

    # Получаем текущее время
    CURRENT_TIME=$(date +"%Y-%m-%d %H:%M:%S")

    # Выводим текущее использование памяти и время для отладки
    echo "Current memory usage: $MEMORY_USAGE%"
    echo "Current time: $CURRENT_TIME"

    # Проверяем, превышает ли использование памяти порог
    if [ "$MEMORY_USAGE" -gt "$MEMORY_THRESHOLD" ]; then
        # Отправляем HTTP запрос на API с информацией об использовании памяти и текущем времени
        curl -X POST -H 'Content-Type: application/json' -d "{\"memory_usage\": $MEMORY_USAGE, \"current_time\": \"$CURRENT_TIME\"}" $API_URL
    fi
        # Ожидаем указанное количество секунд перед повторной проверкой
    sleep $SLEEP_INTERVAL
done
