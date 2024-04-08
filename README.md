# IndigoBot

## Установка

1. Клонируйте репозиторий с помощью Git:

```sh
git clone https://github.com/SergeyKai/IndigoBotD.git
```

Перейдите в папку проекта:
Установите зависимости, используя файл requirements.txt:

```
pip install -r requirements.txt
```


Запустите миграции базы данных:

```
python manage.py migrate
```
## .env
В корне проекта создайте файл .env в который необходимо добавить 2 значения 
```python
SECRET_KEY='django_secret_key'  
TOKEN_BOT='example_token'
```

SECRET_KEY для Django проекта можно сгенерировать на сайте:  
TOKEN_BOT необходимо получить у BotFather
## Запуск

Запуск локальный сервер:
```
python manage.py runserver
```

После запуска сервера, проект будет доступен по адресу `http://127.0.0.1:8000/`

Запуск бота:
```
python manage.py run_bot
```

Запуск планировщика задач: 
```
python manage.py runapscheduler.py
```
