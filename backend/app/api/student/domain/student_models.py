from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from app.api.shared.domain.document_type import DocumentType

if TYPE_CHECKING:
    from app.api.guardian.domain.guardian_models import Guardian


class StudentBase(SQLModel):
    document_type: Optional[DocumentType] = Field(default=None, nullable=True)
    document_number: Optional[str] = Field(default=None, max_length=50, nullable=True)
    full_name: str = Field(max_length=255, nullable=False)


class StudentCreate(StudentBase):
    guardian_id: Optional[UUID] = Field(default=None)


class StudentUpdate(SQLModel):
    document_type: Optional[DocumentType] = None
    document_number: Optional[str] = None
    full_name: Optional[str] = None
    guardian_id: Optional[UUID] = None


class Student(StudentBase, table=True):
    """
    Represent the `Student` entity persisted in the database.
    """
    __tablename__ = "students"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    guardian_id: UUID = Field(default=None, foreign_key="guardians.id")

    guardian: "Guardian" = Relationship(back_populates="students")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def touch(self):
        """
        Updates the `updated_at` field with the current date and time in UTC.
        """
        self.updated_at = datetime.now(timezone.utc)


class StudentPublic(StudentBase):
    id: UUID
    guardian_id: Optional[UUID]


class StudentsPublic(SQLModel):
    data: list[StudentPublic]
    count: int
