from fastapi import APIRouter

from app.api.role.repository.http.role_routers import router as role_router
from app.api.user.infrastructure.http.auth.auth_routers import router as auth_router
from app.api.user.infrastructure.http.user.user_routers import router as user_router
from app.api.student.infrastructure.http.student_routers import router as student_router

api_router = APIRouter()

api_router.include_router(role_router)
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(student_router)