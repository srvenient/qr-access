from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.api.student.domain.student_models import Student
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import SQLAlchemyAggregateRootRepository
from app.api.deps import SessionDep

# Router para manejar estudiantes
router = APIRouter(prefix="/students", tags=["Student"])


@router.post("/", response_model=Student)
def create_student(student: Student, session: Session = Depends(SessionDep)):
    # Crear un nuevo estudiante
    repo = SQLAlchemyAggregateRootRepository(session, Student)
    repo.save_sync(student)
    return student


@router.get("/", response_model=List[Student])
def list_students(session: Session = Depends(SessionDep)):
    # Listar todos los estudiantes
    repo = SQLAlchemyAggregateRootRepository(session, Student)
    return repo.find_all_sync()


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int, session: Session = Depends(SessionDep)):
    # Obtener un estudiante por su ID
    repo = SQLAlchemyAggregateRootRepository(session, Student)
    student = repo.find_sync(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, session: Session = Depends(SessionDep)):
    # Eliminar un estudiante por su ID
    repo = SQLAlchemyAggregateRootRepository(session, Student)
    deleted = repo.delete_sync(id=student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"deleted": True}
