from fastapi import APIRouter

from app.api.endpoints import post, user

main_router = APIRouter()
for router in (post.router, user.router):
    main_router.include_router(router)
