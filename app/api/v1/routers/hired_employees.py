from fastapi import APIRouter, status, HTTPException
from typing import List

from app.core.database import SessionDep
from app.models.hired_employees import HiringEmployee, HiringEmployeeCreate


router = APIRouter()

@router.post("/hiringemployee/", response_model=HiringEmployee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: HiringEmployeeCreate, session: SessionDep):
    """
    :param employee:
    :param session:
    :return:
    """

    new_employee = HiringEmployee(
        name= employee.name,
        created_at= employee.datetime,
        department_id= employee.department_id,
        job_id= employee.job_id,
    )
    session.add(new_employee)
    session.commit()
    session.refresh(new_employee)

    return new_employee

@router.post("/hiringemployees/batch/", status_code=status.HTTP_201_CREATED)
def create_employees_batch(request: List[HiringEmployeeCreate], session: SessionDep):
    created_records = []

    for idx, item in enumerate(request):
        try:
            if not isinstance(item, HiringEmployeeCreate):
                raise ValueError("Invalid data format")

            new_employee = HiringEmployee(
                name=item.name,
                created_at=item.datetime,
                department_id=item.department_id,
                job_id=item.job_id,
            )

            session.add(new_employee)
            session.flush()
            created_records.append(new_employee.id)

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
