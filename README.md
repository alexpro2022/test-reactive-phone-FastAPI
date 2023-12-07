# Проект social_network-FastAPI:

[![Test Suite](https://github.com/alexpro2022/test-reactive-phone-FastAPI/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/test-reactive-phone-FastAPI/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/alexpro2022/test-reactive-phone-FastAPI/graph/badge.svg?token=jWXqnr3w5Q)](https://codecov.io/gh/alexpro2022/test-reactive-phone-FastAPI)

### Simple RESTful API using FastAPI for a social networking application

[Тестовое задание](https://docs.google.com/document/d/1_ZMjuXB0DnioQW7w30mrsA2WYzcdbWII4omgPvdPGQo/edit)

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
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
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![deepdiff](https://img.shields.io/badge/-deepdiff-464646?logo=deepdiff)](https://github.com/seperman/deepdiff)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

</details>

<br>

## Описание работы

Swagger позволяет осуществлять http-запросы к работающему сервису, тем самым можно управлять постами в рамках политики сервиса (указано в Swagger для каждого запроса).

Неавторизованные пользователи могут получать доступ либо ко всем постам, либо к конкретному посту.

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

## Установка и запуск:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
<h1></h1></details>

<details><summary>Локальный запуск</summary>

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/social_network-FastAPI.git && \
cd social_network-FastAPI && \
cp env_example .env && \
nano .env
```

<details><summary>Uvicorn/SQLite3</summary>

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```

3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```

4. В проекте уже инициализирована система миграций Alembic с настроенной автогенерацией имен внешних ключей моделей и создан файл первой миграции. Чтобы ее применить, необходимо выполнить команду:
```bash
alembic upgrade head
```
Будут созданы все таблицы из файла миграций.

5. Запуск приложения - из корневой директории проекта выполните команду:
```bash
uvicorn app.main:app
```
Сервер Uvicorn запустит приложение по адресу http://127.0.0.1:8000.
Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://127.0.0.1:8000/docs .

6. Остановить Uvicorn можно комбинацией клавиш Ctl-C.
<h1></h1></details>


<details><summary>Docker Compose/PostgreSQL</summary>

2. Из корневой директории проекта выполните команду:
```bash
docker compose -f infra/local/docker-compose.yml up -d --build
```
Проект будет развернут в трех docker-контейнерах (db, web, nginx) по адресу http://localhost.
Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://localhost/docs .

3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f infra/local/docker-compose.yml down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f infra/local/docker-compose.yml down -v
```
<h1></h1></details>

Для создания тестовых постов можно воспользоваться следующими данными:

```json
{
  "title": "Yet New post title.",
  "content": "Yet New post content."
}
```

```json
{
  "title": "Another New post title.",
  "content": "Another New post content."
}
```

[⬆️Оглавление](#оглавление)

</details>

<br>

## Удаление:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr social_network-FastAPI && deactivate
```

[⬆️Оглавление](#оглавление)



## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#Проект-social_network-FastAPI)
