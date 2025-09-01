from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from typing import List

from app.core.database import SessionDep
from app.models.jobs import Job, JobCreate


router = APIRouter()

@router.post("/job", response_model=Job, status_code=status.HTTP_201_CREATED)
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


@router.post("/jobs/batch/", status_code=status.HTTP_201_CREATED)
def create_employees_batch(request: List[JobCreate], session: SessionDep):
    created_records = []

    existing_jobs = session.exec(
        select(Job.job)
    ).all()
    job_names = [job for job in existing_jobs]

    for idx, item in enumerate(request):
        try:
            if not isinstance(item, JobCreate):
                raise ValueError("Invalid data format")
            if item.job in job_names:
                raise ValueError(f"Job name '{item.job}' already exist.")

            new_job = Job(job = item.job)

            session.add(new_job)
            session.flush()
            created_records.append(new_job.id)
            job_names.append(item.job)

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
