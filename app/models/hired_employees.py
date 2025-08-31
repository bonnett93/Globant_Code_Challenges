from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class HiringEmployee(SQLModel, table=True):
    __tablename__ = 'hired_employees'

    id: Optional[int] = Field(primary_key=True, unique=True, index=True)
    name: str = Field(nullable=False)
    datetime: datetime  = Field(nullable=False)
    department_id: str = Field(nullable=False, foreign_key="departments.id")
    job_id: int = Field(nullable=False, foreign_key="jobs.id")
