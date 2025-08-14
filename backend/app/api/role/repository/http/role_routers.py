from fastapi import APIRouter, HTTPException

from app.api.deps import RoleAggregateRepositoryDep
from app.api.role.application import role_service
from app.api.role.domain.role_models import Role, RoleCreate

router = APIRouter(prefix="/roles", tags=["Role"])


@router.get("/health", summary="Check role service health")
async def health_check():
    return {"status": "Role service is healthy"}


@router.get("/{role_id}", summary="Get role by ID")
async def get_role(role_id: str, repository=RoleAggregateRepositoryDep):
    role = await repository.find_async(_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/", summary="Get all roles")
async def get_all_roles(repository=RoleAggregateRepositoryDep):
    roles = await repository.find_all_async()
    return {"roles": roles, "count": len(roles)}


@router.post("/", summary="Create a new role")
async def create_role(role_create: RoleCreate, repository=RoleAggregateRepositoryDep):
    role = Role(**role_create.model_dump())
    await repository.save_async(role)
    return role
