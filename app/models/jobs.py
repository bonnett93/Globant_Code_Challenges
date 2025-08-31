from typing import Optional
from sqlmodel import SQLModel, Field

class Job(SQLModel, table=True):
    __tablename__ = 'jobs'

    id: Optional[int] = Field(primary_key=True, unique=True, index=True)
    job: str = Field(nullable=False, unique=True)
