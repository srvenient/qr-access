from fastapi import APIRouter, HTTPException

from app.api.deps import UserAggregateRepositoryDep
from app.api.user.domain.user_models import UserCreate, User

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/health", summary="Check user service health")
async def health_check():
    return {"status": "User service is healthy"}


@router.get("/{user_id}", summary="Get user by ID")
async def get_user(user_id: str, repository=UserAggregateRepositoryDep):
    user = await repository.find_async(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", summary="Create a new user")
async def create_user(user_create: UserCreate, repository=UserAggregateRepositoryDep):
    user = User(**user_create.model_dump())
    await repository.save_async(user)
    return user
