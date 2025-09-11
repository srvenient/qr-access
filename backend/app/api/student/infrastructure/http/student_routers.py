from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from starlette import status
from fastapi.responses import Response

from app.api.student.application import student_services
from app.api.student.domain.student_models import Student, StudentUpdate, StudentPublic
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.deps import SessionDep, StudentAggregateRepositoryDep

# Router para manejar estudiantes
router = APIRouter(prefix="/students", tags=["Student"])


@router.put("/{student_id}", response_model=StudentPublic)
async def update_student(
        student_id: UUID,
        student_update: StudentUpdate,
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep,
):
    student = await student_repository.find_async(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    student.touch()

    await student_repository.save_async(student)

    return StudentPublic.from_orm(student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
        student_id: UUID,
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep,
):
    deleted = await student_repository.delete_async(id=student_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[StudentPublic])
async def get_all_students(
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep,
):
    students = await student_repository.find_all_async()
    return [StudentPublic.model_validate(student) for student in students]


@router.get("/{student_id}", response_model=StudentPublic)
async def get_student_by_id(
        student_id: UUID,
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep,
):
    student = await student_repository.find_async(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentPublic.model_validate(student)


@router.post("/", response_model=StudentPublic, status_code=status.HTTP_201_CREATED)
async def create_student(
        student_create: Student,
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep,
):
    await student_repository.save_async(student_create)
    return StudentPublic.model_validate(student_create)
