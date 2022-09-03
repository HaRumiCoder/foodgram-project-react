# Foodgram ![](https://github.com/HaRumiCoder/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Проект доступен по ссылке http://84.201.176.127/


___
## Описание проекта

Проект Foodgram позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

В данном репозитории представлен бэкенд в виде API, фронтенд проекта, докер файлы для создания контейнеров, а также присутствует настроенный workflow


___
## Backend

Хранится в папке backend, реализован на Django Rest Framework

примеры запросов API:

*http://84.201.176.127/api/users/ метод GET*

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "vpupkin@yandex.ru",
            "id": 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
        },
        {
            "email": "shilsny@yandex.ru",
            "id": 3,
            "username": "HaRumiAdmin",
            "first_name": "Harumi",
            "last_name": "Coder",
            "is_subscribed": false
        }
    ]
}
```

*http://84.201.176.127/api/recipes/ метод GET*

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 32,
            "ingredients": [
                {
                    "id": 1081,
                    "amount": 400,
                    "name": "мука",
                    "measurement_unit": "г"
                },
                {
                    "id": 2182,
                    "amount": 40,
                    "name": "яйца куриные",
                    "measurement_unit": "г"
                },
                {
                    "id": 252,
                    "amount": 500,
                    "name": "вода",
                    "measurement_unit": "г"
                }
            ],
            "tags": [
                1
            ],
            "image": "/media/recipes/8ebc8e10-18d6-43f9-8a3d-f020b8e122fd.png",
            "name": "Блинчики",
            "text": "Все смешайте и пожарьте)",
            "cooking_time": 20,
            "author": {
                "email": "shilsny@yandex.ru",
                "id": 3,
                "username": "HaRumiAdmin",
                "first_name": "Harumi",
                "last_name": "Coder",
                "is_subscribed": false
            },
            "is_favorited": false,
            "is_in_shopping_cart": false
        }
    ]
}
```

*http://84.201.176.127/api/recipes/32/favorite/ метод POST*

```json
{
    "id": 32,
    "name": "Блинчики",
    "image": "/media/recipes/8ebc8e10-18d6-43f9-8a3d-f020b8e122fd.png",
    "cooking_time": 20
}
```

*http://84.201.176.127/api/tags/ метод POST*

```json
[
    {
        "id": 2,
        "name": "Обед",
        "color": "#00BFFF",
        "slug": "lunch"
    },
    {
        "id": 3,
        "name": "Ужин",
        "color": "#B22222",
        "slug": "dinner"
    },
    {
        "id": 1,
        "name": "Завтрак",
        "color": "#7CFC00",
        "slug": "breakfast"
    }
]
```

Полная документация доступна по адресу http://84.201.176.127/api/docs/


___
## Frontend

Хранится в папке frontend. Представляет собой одностраничное приложение на фреймворке React


___
## Инфраструктура

Возможно развернуть проект локально на своем компьютере в контейнерах Docker:

- Склонируйте папку проекта на ваш компьютер

``` git clone https://github.com/HaRumiCoder/foodgram-project-react.git ```

- Перейдите в папку с файлом docker-compose.yaml

``` cd infra/ ```

- Создайте контейнеры (web, db, nginx, frontend)

``` docker-compose up ```

- В контейнере web сделайте миграции, создайте суперюзера django и соберите статику в папку api_yamdb/static/

``` docker-compose exec web python manage.py makemigrations ```

``` docker-compose exec web python manage.py migrate ```

``` docker-compose exec web python manage.py createsuperuser ```

``` docker-compose exec web python manage.py collectstatic --no-input ```


Проект работает с базой данных PostgreSQL, поэтому для развертывания контейнеров необходимо иметь файл с переменными окружения .env по следующему образцу:

```yaml
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
DB_HOST=db
DB_PORT=5432
```


____
## Workflow 

В репозитории настроены приложения Continuous Integration и Continuous Deployment

Реализованы:

- автоматический запуск тестов
- обновление образов на Docker Hub
- автоматический деплой на боевой сервер при пуше в главную ветку main

___
## Автор

Софья Шилова https://github.com/HaRumiCoder
