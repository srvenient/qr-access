from typing import Any, Coroutine
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app.api.deps import StudentAggregateRepositoryDep
from app.api.shared.aggregate.infrastructure.repository.sql.sql_alchemy_aggregate_root_repository import \
    SQLAlchemyAggregateRootRepository
from app.api.student.domain.student_models import Student


async def delete_student(
        student_id: UUID,
        student_repository: SQLAlchemyAggregateRootRepository[Student] = StudentAggregateRepositoryDep
) -> JSONResponse:
    if not student_repository.exists_async(id=student_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await student_repository.delete_async(id=student_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
