from fastapi import APIRouter, status

from app.models.hired_employees import HiringEmployee, HiringEmployeeCreate
from app.core.database import SessionDep


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
