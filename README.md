# test-reactive-phone-FastAPI
[Тестовое задание](https://docs.google.com/document/d/1AcmooPkbqhpI6lHGiyLOqEyN-t1nnbR9BFO8M6EfRtE/edit) для Reactive Phone - Junior Backend разработчик (в международный проект)

<br>

## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
- [Автор](#автор)

<br>

## Технологии:
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![asyncio](https://img.shields.io/badge/-asyncio-464646?logo=python)](https://docs.python.org/3/library/asyncio.html)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)](https://docs.pydantic.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v2.0-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![APScheduler](https://img.shields.io/badge/-APScheduler-464646?logo=APScheduler)](https://apscheduler.readthedocs.io/en/stable/index.html)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest)](https://pypi.org/project/pytest-asyncio/)
[![coverage](https://img.shields.io/badge/-coverage-464646?logo=coverage)](https://coverage.readthedocs.io/en/latest/index.html)
[![deepdiff](https://img.shields.io/badge/-deepdiff-464646?logo=deepdiff)](https://zepworks.com/deepdiff/6.3.1/diff.html)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)

[⬆️Оглавление](#оглавление)
</details>

<br>

## Описание работы:


[⬆️Оглавление](#оглавление)

<br>

## Установка и запуск:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
```bash
docker --version && docker-compose --version
```
<h1></h1>
</details>

<details><summary>Локальный запуск: Docker Compose</summary>

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):
```bash
git clone https://github.com/alexpro2022/test-reactive-phone-FastAPI.git
cd test-reactive-phone-FastAPI
cp env_example .env
nano .env
```

2. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/docker-compose.yml up -d --build
```
Проект будет развернут в docker-контейнерах `db, backend` по адресу http://localhost.

Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://localhost/docs.

3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f docker/docker-compose.yml down
```
Если также необходимо удалить тома базы данных, статики и медиа:
```bash
docker compose -f docker/docker-compose.yml down -v
```

[⬆️Оглавление](#оглавление)
</details>

<br>

## Удаление:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr test-reactive-phone-FastAPI
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#test-reactive-phone-FastAPI)
