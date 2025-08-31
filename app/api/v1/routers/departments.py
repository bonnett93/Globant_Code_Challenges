from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from app.models.departments import Department, DepartmentCreate
from app.core.database import SessionDep


router = APIRouter()

@router.post("/departments/", response_model=Department, status_code=status.HTTP_201_CREATED)
async def create_department(department: DepartmentCreate, session: SessionDep):
    """
    :param department:
    :param session:
    :return:
    """
    existing_department = session.exec(
        select(Department).where(Department.department == department.department)
    ).first()

    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Department name '{department.department}' already exist."
        )

    new_department = Department(department=department.department)
    session.add(new_department)
    session.commit()
    session.refresh(new_department)

    return new_department
