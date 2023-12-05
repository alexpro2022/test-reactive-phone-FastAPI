from datetime import datetime as dt

from fastapi import APIRouter

from app import schemas
from app.core import authorized, settings
from app.models import Post
from app.services import post_service

router = APIRouter(prefix='/post', tags=['Posts'])

SUM_ALL_POSTS = 'Возвращает список всех постов.'
SUM_ALL_USER_POSTS = ('Возвращает список всех постов '
                      'выполняющего запрос пользователя.')
SUM_POST = 'Возвращает пост по ID.'
SUM_CREATE_POST = 'Создание нового поста.'
SUM_UPDATE_POST = 'Редактирование поста.'
SUM_DELETE_POST = 'Удаление поста.'
SUM_LIKE_POST = 'Поставить LIKE посту.'
SUM_DISLIKE_POST = 'Поставить DISLIKE посту.'


@router.get(
    '/',
    response_model=list[schemas.PostResponse],
    response_model_exclude_none=True,
    summary=SUM_ALL_POSTS,
    description=(f'{settings.ALL_USERS} {SUM_ALL_POSTS}'))
async def get_all_posts(ps: post_service) -> list[Post]:
    return await ps.get_all()


@router.post(
    '/',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_CREATE_POST,
    description=(f'{settings.AUTH_ONLY} {SUM_CREATE_POST}'))
async def create_post(payload: schemas.PostCreate, ps: post_service, user: authorized) -> Post:
    return await ps.create(payload, author_id=user.id)


@router.get(
    '/{post_id}',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_POST,
    description=(f'{settings.ALL_USERS} {SUM_POST}'))
async def get_post(post_id: int, ps: post_service) -> Post:
    return await ps.get_or_404(post_id)


@router.put(
    '/{post_id}',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_UPDATE_POST,
    description=(f'{settings.AUTH_ONLY} {SUM_UPDATE_POST}'))
async def update_post(post_id: int, payload: schemas.PostUpdate, ps: post_service, user: authorized) -> Post:
    return await ps.update(post_id, payload, user, updated=dt.now())


@router.delete(
    '/{post_id}',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_DELETE_POST,
    description=(
        f'{settings.SUPER_ONLY} {SUM_DELETE_POST}'))
async def delete_post(post_id: int, ps: post_service, user: authorized) -> Post:
    return await ps.delete(post_id, user)


@router.get(
    '/like/{post_id}',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_LIKE_POST,
    description=(f'{settings.AUTH_ONLY} {SUM_LIKE_POST}'))
async def like_post_(post_id: int, ps: post_service, user: authorized) -> Post:
    return await ps.like_dislike_post(post_id, user)


@router.get(
    '/dislike/{post_id}',
    response_model=schemas.PostResponse,
    response_model_exclude_none=True,
    summary=SUM_DISLIKE_POST,
    description=(f'{settings.AUTH_ONLY} {SUM_DISLIKE_POST}'))
async def dislike_post_(post_id: int, ps: post_service, user: authorized) -> Post:
    return await ps.db.like_dislike_post(post_id, user, False)


@router.get(
    '/my_posts/',
    response_model=list[schemas.PostResponse],
    response_model_exclude_none=True,
    summary=SUM_ALL_USER_POSTS,
    description=(f'{settings.AUTH_ONLY} {SUM_ALL_USER_POSTS}'))
async def get_user_posts_(ps: post_service, user: authorized) -> list[Post]:
    return await ps.db.get_user_posts(user)
