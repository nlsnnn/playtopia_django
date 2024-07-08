# Playtopia

Онлайн магазин компьютерных игр(ключей steam), созданный в целях практики Django.

## Стек
* Python
* Django - серверная часть
* HTML, CSS, JavaScript - фронтенд, используется шаблонизатор Django
* Celery - асинхронные задачи, такие как отправка писем на почту
* Redis - брокер сообщений и кэширование

## Требования

Убедитесь, что у вас установлены следующие инструменты:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Запуск проекта

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/playtopia.git
    cd playtopia
    ```

2. Создайте и настройте файл окружения `.env`:

    ```bash
    cp .env.example .env
    ```

    Отредактируйте файл `.env`

3. Запустите контейнеры:

    ```bash
    docker-compose up --build
    ```

4. Создайте суперпользователя:

    ```bash
    docker exec -it playtopia-backend python manage.py createsuperuser
    ```
