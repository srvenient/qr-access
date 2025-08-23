from fastapi import APIRouter

from app.api.deps import CurrentUser

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me")
async def read_users_me(current_user: CurrentUser):
    return current_user
