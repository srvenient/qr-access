from fastapi import APIRouter

from app.api.role.repository.http.role_routers import router as role_router
from app.api.user.infrastructure.http.user_routers import router as user_router

api_router = APIRouter()

api_router.include_router(role_router)
api_router.include_router(user_router)
