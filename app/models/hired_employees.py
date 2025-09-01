from typing import Optional
from pydantic import field_validator
from sqlmodel import SQLModel, Field
from datetime import datetime


class HiringEmployee(SQLModel, table=True):
    __tablename__ = 'hired_employees'

    id: Optional[int] = Field(primary_key=True, unique=True, index=True)
    name: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False, alias="datetime")
    department_id: int = Field(nullable=False, foreign_key="departments.id")
    job_id: int = Field(nullable=False, foreign_key="jobs.id")

    @field_validator('created_at')
    @classmethod
    def validate_created_at(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("Creation date must be in ISO 8601 format")


class HiringEmployeeCreate(SQLModel):
    name: str
    datetime: datetime
    department_id: int
    job_id: int
