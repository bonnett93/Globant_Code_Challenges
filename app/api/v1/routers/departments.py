from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from typing import List

from app.core.database import SessionDep
from app.models.departments import Department, DepartmentCreate


router = APIRouter()

@router.post("/department/", response_model=Department, status_code=status.HTTP_201_CREATED)
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

@router.post("/departments/batch/", status_code=status.HTTP_201_CREATED)
def create_departments_batch(request: List[DepartmentCreate], session: SessionDep):
    created_records = []

    existing_departments = session.exec(
        select(Department.department)
    ).all()
    department_names = [dep for dep in existing_departments]

    for idx, item in enumerate(request):
        try:
            if not isinstance(item, DepartmentCreate):
                raise ValueError("Invalid data format")
            if item.department in department_names:
                raise ValueError(f"Department name '{item.department}' already exist.")

            new_department = Department(department=item.department)
            session.add(new_department)
            session.flush()
            created_records.append(new_department.id)
            department_names.append(item.department)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Problem at index {idx} {e}"
            )

    if created_records:
        session.commit()

    return {
        "success_count": len(created_records),
        "created_ids":created_records,
    }
