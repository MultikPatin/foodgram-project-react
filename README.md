# Диломный проект Foodgram

Проект 'Продуктовый помощник' реализует сайт кулинарных рецептов,
в котором вы можете создавать рецепты, подписываться на понравившихся
авторов, подобрать себе коллекцию любимых рецептов и другой функционал.

## Проект запускается в 4 контейнерах

    nginx
    backend
    frontend
    db

## Авторизация по токену

Все запросы от имени пользователя должны выполняться с заголовком

    "Authorization: Token TOKENVALUE"

## Необходимые инструменты для запуска

    docker
    docker-compose

## Запуск приложения

Перед запуском необходимо создать файл .env с переменными в
корневом каталоге

    POSTGRES_DB
    POSTGRES_USER
    POSTGRES_PASSWORD
    DB_HOST
    DB_PORT
    SECRET_KEY
    ALLOWED_HOSTS
    DEBUG

## Запуск контейнеров

перейти в католог /infra/ и выполнить

```bash
docker-compose up -d --build
```

При запуске контейнеров БД создаётся атоматически и так же теги и
ингрилиенты автоматически заполняются данныйми из файлов:

    /backend/test_data/ingredients.csv
    /backend/test_data/tags.csv


### Стек используемых технологий

    Python 3.9
    Django 4.2.3
    djangorestframework 3.14.0
    Docker
    PostgreSQL 13.10
    gunicorn 20.1.0
    CI
    nginx 1.19.3
    djoser 2.2.0

### Доступные эндпоинты

#### docs

            docs/                           # Документация проекта

#### admin

            admin/                          # Панель администратора

#### recipes

    GET     recipes/                        # Получить список рецептов
    POST    recipes/                        # Создание рецепта
    GET     recipes/{id}/                   # Получение рецепта по id
    PATCH   recipes/{id}                    # Изменение рецепта
    DELETE  recipes/{id}/                   # Удаление рецепта
    GET     recipes/download_shopping_cart/ # Скачать список покупок
    POST    recipes/{id}/shopping_cart      # Добавить рецепт в список покупок
    DELETE  recipes/{id}/shopping_cart      # Удаление рецепта из списка покупок
    POST    recipes/{id}/favorite/          # Добавить рецепт в избранное
    DELETE  recipes/{id}/favorite/          # Удаление рецепта из избранного

#### users

    POST    users/                          # Регистрация пользователя
    GET     users/                          # Получение списка пользователей
    GET     users/{id}/                     # Получение пользователя по id
    GET     users/me/                       # Получение текущего пользователя
    POST    users/set_password/             # Изменение пароля текущего пользователя
    GET     users/subscriptions/            # Мои подписки
    POST    users/{id}/subscribe/           # Подписаться на пользователя
    DELETE  users/{id}/subscribe/           # Отписаться от пользователя
    POST    auth/token/login/               # Получить токен авторизации
    POST    auth/token/logout/              # Удаление токена

#### ingredients

    GET     ingredients/                    # Получить список ингредиентов
    GET     ingredients/{id}/               # Получить ингредиент по id

#### tags

    GET     tags/                           # Получить список ингредиентов
    GET     tags/{id}/                      # Получение тега по id
