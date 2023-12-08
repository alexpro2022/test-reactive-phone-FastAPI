# Проект социальной сети:

[![Test Suite](https://github.com/alexpro2022/test-reactive-phone-FastAPI/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/test-reactive-phone-FastAPI/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/alexpro2022/test-reactive-phone-FastAPI/graph/badge.svg?token=jWXqnr3w5Q)](https://codecov.io/gh/alexpro2022/test-reactive-phone-FastAPI)


[Тестовое задание](https://docs.google.com/document/d/1_ZMjuXB0DnioQW7w30mrsA2WYzcdbWII4omgPvdPGQo/edit)

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Запуск тестов](#запуск-тестов)
- [Запуск приложения](#запуск-приложения)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>

## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![asyncio](https://img.shields.io/badge/-asyncio-464646?logo=python)](https://docs.python.org/3/library/asyncio.html)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![FastAPI_Users](https://img.shields.io/badge/-FastAPI--Users-464646?logo=fastapi-users)](https://fastapi-users.github.io/fastapi-users/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v2.0-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=asyncpg)](https://pypi.org/project/asyncpg/)
[![aioredis](https://img.shields.io/badge/-aioredis-464646?logo=redis)](https://aioredis.readthedocs.io/en/latest/)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![celery](https://img.shields.io/badge/-Celery-464646?logo=celery)](https://docs.celeryq.dev/en/stable/)
[![rabbitmq](https://img.shields.io/badge/-RabbitMQ-464646?logo=rabbitmq)](https://www.rabbitmq.com/)
[![flower](https://img.shields.io/badge/-Flower-464646?logo=flower)](https://flower.readthedocs.io/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

</details>

<br>

## Описание работы

Приложение состоит из:

1. Асинхронного httpx-клиента для криптобиржи Deribit:

через определенный интервал времени (задается пользователем) httpx-клиент забирает с биржи текущую цену BTC и ETH и логирует тикер валюты, текущую цену и время в UNIX (данные можно посмотреть по ссылке http://127.0.0.1:5555/tasks). Асинхронный клиент работает по протоколу HTTP/2 в фоновой периодической celery-задаче.

3. Социальной сети:
Swagger позволяет осуществлять http-запросы к работающему сервису, тем самым можно управлять постами в рамках политики сервиса (указано в Swagger для каждого запроса).

Неавторизованные пользователи могут получать доступ на чтение либо ко всем постам, либо к конкретному посту.

Авторизованный пользователь дополнительно может создавать посты, редактировать и удалять свои посты (админ имеет права доступа к любым постам), ставить лайки и дислайки для любых постов, кроме своих. Для доступа к этим функциям необходимо авторизоваться в Swagger, используя:
  - либо учетные данные из **.env**-файла (этот пользователь с правами админа создается программно при запуске приложения)
  - либо учетные данные нового зарегистрированного пользователя - зарегистрироваться можно через эндпоинт /auth/register  в Swagger:

Авторизация:
 1. Нажмите:
    - на символ замка в строке любого эндпоинта или
    - на кнопку `Authorize` в верхней части Swagger.
     Появится окно для ввода логина и пароля.

 2. Введите учетные данные в поля формы:
    - в поле `username` — адрес почты (например значение переменной окружения `ADMIN_EMAIL`),
    - в поле `password` — пароль (например значение переменной окружения `ADMIN_PASSWORD`).

    В выпадающем списке `Client credentials location` оставьте значение `Authorization header`,
    остальные два поля оставьте пустыми; нажмите кнопку `Authorize`.
Если данные были введены правильно, и таблица в БД существует — появится окно с подтверждением авторизации, нажмите `Close`.
Чтобы разлогиниться — перезагрузите страницу.

[⬆️Оглавление](#оглавление)

<br>

## Установка приложения:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
<h1></h1></details>

<br>

Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/test-reactive-phone-FastAPI.git
cd test-reactive-phone-FastAPI
cp env_example .env
nano .env
```

[⬆️Оглавление](#оглавление)

<br>

## Запуск тестов:

Из корневой директории проекта выполните команду:
```bash
docker build -f ./docker/test.Dockerfile -t social_network_tests .
docker run --name tests social_network_tests
docker container rm tests
docker rmi social_network_tests
```

[⬆️Оглавление](#оглавление)

<br>

## Запуск приложения:

1. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/docker-compose.yml up -d --build
```
  Проект будет развернут в docker-контейнерах по адресу http://127.0.0.1:8000.

  Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://127.0.0.1:8000/docs .

  Мониторинг фоновых задач Celery осуществляется по адресу: http://127.0.0.1:5555/tasks .

2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f docker/docker-compose.yml down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/docker-compose.yml down -v
```

[⬆️Оглавление](#оглавление)

<br>

## Удаление приложения:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr test-reactive-phone-FastAPI
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#проект-социальной-сети)
