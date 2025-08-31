from typing import Optional
from sqlmodel import SQLModel, Field

class Department(SQLModel, table=True):
    __tablename__ = 'departments'

    id: Optional[int] = Field(default=None, primary_key=True, unique=True, index=True)
    department: str = Field(nullable=False, unique=True)

class DepartmentCreate(SQLModel):
    department: str