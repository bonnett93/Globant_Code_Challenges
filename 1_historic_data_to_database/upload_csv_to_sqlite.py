from sqlalchemy import delete
from sqlmodel import create_engine, Session, SQLModel
from app.models import jobs, departments,hired_employees
import csv
from datetime import datetime


engine = create_engine("postgresql+psycopg2://postgres:1q2w3e4r5t@:5432/globant_resources")
engine.connect()
session = Session(bind=engine)
SQLModel.metadata.create_all(engine)

session.exec(delete(jobs.Job))
session.exec(delete(departments.Department))
session.exec(delete(hired_employees.HiringEmployee))

session.commit()

# ---
jobs_file = "../data/jobs.csv"
file_open = open(jobs_file, "r")
csv_reader = csv.reader(file_open)

file_open.seek(0)
for row in csv_reader:
    new_job = jobs.Job(id=int(row[0]), job=row[1])
    session.add(new_job)

session.commit()

# ---
deps_file = "../data/departments.csv"
file_open = open(deps_file, "r")
csv_reader = csv.reader(file_open)

file_open.seek(0)
for row in csv_reader:
    new_dep = departments.Department(id=int(row[0]), department=row[1])
    session.add(new_dep)

session.commit()

# ---
employee_file = "../data/hired_employees.csv"
file_open = open(employee_file, "r")
csv_reader = csv.reader(file_open)

file_open.seek(0)
for idx, row in enumerate(csv_reader):
    try:
        new_employee = hired_employees.HiringEmployee(id=int(row[0]), name=row[1], created_at=datetime.fromisoformat(row[2]),
                                                      department_id=int(row[3]), job_id=int(row[4]))
    except ValueError as e:
        continue
    session.add(new_employee)

session.commit()

session.close()


