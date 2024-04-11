# Описание

    Файл сервера на flask с тремя методами GET, POST, PUT
    находится в папке api
    Дефолтный порт на котором раотает приложение 8080, так же его можно изменить в фале .env

    База данных используемая в данном задании - mongodb
    Дефолтный порт 27017
    Дефолтные названия базы данных и коллекции так же можно изменить в  фале .env

# Разворачиваем сервер и базу данных

## Создаем файл переменных среды

```bash
$ cp .env.example .env
```

## Запускаем контейнеры с flask-сервером и mongodb

```bash
$ docker-compose up -d
```

# Запуск скрипта для отслеживания потребления памяти

    Параметры для настройки url на который будут отправлены данные (API_URL), значения при привышении которого сработает скрипт отправки (MEMORY_THRESHOLD) и время между проверкой значения загруженности памяти (SLEEP_INTERVAL) указаны в .env файле

     По умолчанию скрипт настроен так, что отправляет процент использованной памяти и текущее время при привышении 20%(MEMORY_THRESHOLD) на localhost flask сервер (API_URL)

## Bash (Опционально/ рекомендуется)

### Сделаем файл скрипта исполняемым в системе

```bash
$ chmod +x mem-control.sh
```

### Запустим bash скрипт

```bash
$ ./mem-control.sh
```

## Python (Опционально/ не рекомендуется)

    Не рекомендуется использовать этот скрипт так как он использует не станадртные библиотеки, которые необходимо установить дополнительно

```bash
$ python mem-monitor.py
```

# Проверка работы

## GET

```bash
$  curl http://localhost:8080/
```

## POST

    Замените значения key и value на ваши собственные

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"key1": "value1", "key2": "value2"}' http://127.0.0.1:8080/
```

## PUT

    Замените updated_key и updated_value на новые значения, а так же data_id на id записи к котрой хотите применить изменения

```bash
$ curl -X PUT -H "Content-Type: application/json" -d '{"updated_key": "updated_value"}' http://127.0.0.1:8080/data_id
```