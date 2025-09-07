from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


# Enumeración de tipos de documento válidos
class DocumentType(str, Enum):
    ID_CARD = "ID_Card"           # Cédula de ciudadanía
    FOREIGN_ID = "Foreign_ID"     # Cédula de extranjería
    PASSPORT = "Passport"         # Pasaporte
    CITIZEN_CARD = "Citizen_Card" # Tarjeta de identidad


# Base común de atributos de un estudiante
class StudentBase(SQLModel):
    document_type: Optional[DocumentType] = Field(default=None, nullable=True)
    document_number: Optional[str] = Field(default=None, max_length=50, nullable=True)
    full_name: str = Field(max_length=255, nullable=False)


# Modelo para creación de estudiantes (entrada API)
class StudentCreate(StudentBase):
    guardian_id: Optional[UUID] = Field(default=None)


# Modelo para actualización parcial de estudiantes (entrada API)
class StudentUpdate(SQLModel):
    document_type: Optional[DocumentType] = None
    document_number: Optional[str] = None
    full_name: Optional[str] = None
    guardian_id: Optional[UUID] = None


# Entidad principal Student mapeada a la tabla `students`
class Student(StudentBase, table=True):
    """
    Representa la entidad `Student` persistida en la base de datos.
    """
    __tablename__ = "students"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    guardian_id: Optional[UUID] = Field(default=None, foreign_key="guardians.id")

    # Relación con la entidad Guardian
    guardian: Optional["Guardian"] = Relationship(back_populates="students")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def touch(self):
        """
        Actualiza el campo `updated_at` con la fecha y hora actual en UTC.
        """
        self.updated_at = datetime.now(timezone.utc)


# Modelo de salida para un estudiante en la API
class StudentPublic(StudentBase):
    id: UUID
    guardian_id: Optional[UUID]


# Modelo de salida para listar estudiantes en la API (colección)
class StudentsPublic(SQLModel):
    data: list[StudentPublic]
    count: int
