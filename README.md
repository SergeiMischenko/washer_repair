![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django?style=plastic&logo=Python)
<h1 align="center">Сайт по ремонту стиральных машин</h1>

<h4 align="center">Этот проект представляет собой веб-сайт для компании по ремонту стиральных машин, разработанный на Django. Сайт позволяет клиентам оставлять заявки на ремонт, а мастерам управлять этими заявками. Проект развернут на VPS сервере и настроен для работы с Nginx и Gunicorn. Адрес сайта: https://orel-tech.ru</h4>

___
<h2 align="center">Функционал</h2>

- **Оставление заявки**: Клиенты могут оставить заявку на ремонт через форму на сайте. После отправки заявки выводится Notification на сайте - чтобы уведомить клиента что заявка отправлена или возникла ошибка.

- **Управление заявками**: Мастера получают уведомления о новых заявках с минимальным описанием в Telegram-группе через бота и могут перейти по ссылке в админ-панель где они могут более подробнее изучить заявку либо назначить мастера и измененить статус заявки.

- **Отслеживание статуса заявки**: Клиенты могут отслеживать статус своих заявок, введя своё имя и телефон на сайте в форме "Моя заявка". Отображается информация о всех заявках клиента и текущем статусе ремонта.

- **Сбор отзывов**: После завершения ремонта. Мастер изменяет статус заявки, а клиент получает письмо на почту с уникальной ссылкой для оставления отзыва с рейтингом, используется уникальный Token - клиента, чтобы исключить возможность оставления отзывов посторонними лицами.

- **Адаптивный дизайн**: Сайт полностью адаптирован для работы на любых устройствах, включая планшеты и мобильные телефоны.
  
___
<h2 align="center">Стек технологий</h2>

- **Backend**: Python, Django
- **Frontend**: HTML, HTMX, CSS, JavaScript, Bootstrap
- **База данных**: PostgreSQL
- **Системы и инструменты**: Docker, Nginx, Gunicorn, VPS сервер
- **Библиотеки и модули**: python-telegram-bot, asyncio и другие вспомогательные библиотеки.

___
<h2 align="center">Установка и запуск локально без Docker</h2>

1. **Клонировать репозиторий:**
    ```bash
    git clone https://github.com/SergeiMischenko/washer_repair.git

2. **Перейти в директорию проекта:**
    ```bash
    cd washer_repair

3. **Создать и активировать виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate # для Linux/Mac
    venv\Scripts\activate # для Windows

4. **Установить зависимости:**
    ```bash
    pip install -r requirements.txt

5. **Создать в директории docker/env/.env.dev и заполнить его своими данными**
   ```env
    SECRET_KEY="СВОЙ КЛЮЧ DJANGO"

    DEBUG=True
    
    ALLOWED_HOSTS="127.0.0.1 localhost"
    SITE_URL="http://127.0.0.1:8000"
    CSRF_TRUSTED_ORIGINS="http://127.0.0.1 http://localhost"
    
    TELEGRAM_BOT_TOKEN="ТОКЕН ВАШЕГО ТЕЛЕГРАМ БОТА"
    TELEGRAM_CHAT_ID="ID ЧАТА ГДЕ НАХОДИТСЯ БОТ"
    
    # Database
    POSTGRES_DB=NAME_DB
    POSTGRES_USER=NAME_USER_DB
    POSTGRES_PASSWORD=PASSWORD
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    
    DJANGO_SETTINGS_MODULE=washer_repair.settings
    
    # Email settings Если нужен этот функционал
    EMAIL_HOST="smtp.yandex.ru"
    EMAIL_HOST_USER="ИМЯ ЮЗЕРА YANDEX"
    EMAIL_HOST_PASSWORD="ПАРОЛЬ SMTP"
    EMAIL_PORT=465
    EMAIL_USE_SSL=True

6. **Выполнить миграции базы данных:**
    ```bash
    python manage.py migrate

7. **Запустить сервер разработки:**
    ```bash
    python manage.py runserver

___
<h2 align="center">Установка и запуск локально с Docker</h2>

1. **Клонировать репозиторий:**
    ```bash
    git clone https://github.com/SergeiMischenko/washer_repair.git

2. **Перейти в директорию проекта:**
    ```bash
    cd washer_repair

3. **Выполнить пункт 5, который выше**
   
4. **Построить и запустить контейнеры с помощью Docker Compose:**
   ```bash
   docker-compose up --build

5. **Доступ к приложению:**
   
   После завершения всех вышеуказанных шагов, приложение будет доступно по адресу http://127.0.0.1:8000.

___
<h4 align="center">Лицензия</h4>
Все права защищены. Этот проект является коммерческим и не может быть изменен или распространен без явного разрешения владельца.
