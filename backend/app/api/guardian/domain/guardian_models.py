from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.api.student.domain.student_models import Student


class GuardianBase(SQLModel):
    document_type: Optional[str] = Field(default=None, max_length=50, nullable=True)
    document_number: Optional[str] = Field(default=None, max_length=50, nullable=True)
    full_name: str = Field(max_length=255, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20, nullable=True)
    email: Optional[str] = Field(default=None, max_length=255, nullable=True)


class GuardianCreate(GuardianBase):
    pass


class GuardianUpdate(SQLModel):
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Guardian(GuardianBase, table=True):
    """
    Represent the `Guardian` entity persisted in the database.
    """
    __tablename__ = "guardians"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)

    students: List["Student"] = Relationship(back_populates="guardian")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def touch(self):
        """
        Updates the `updated_at` field with the current date and time in UTC.
        """
        self.updated_at = datetime.now(timezone.utc)


class GuardianPublic(GuardianBase):
    id: UUID


class GuardiansPublic(SQLModel):
    data: List[GuardianPublic]
    count: int
