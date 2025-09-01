from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from app.core.database import SessionDep
from app.models.jobs import Job, JobCreate


router = APIRouter()

@router.post("/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, session: SessionDep):
    """
    :param job:
    :param session:
    :return:
    """
    existing_job = session.exec(
        select(Job).where(Job.job == job.job)
    ).first()

    if existing_job:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Job name '{job.job}' already exist."
        )

    new_job = Job(job = job.job)
    session.add(new_job)
    session.commit()
    session.refresh(new_job)
    return new_job
