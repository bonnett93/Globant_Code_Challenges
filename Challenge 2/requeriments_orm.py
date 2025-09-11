# example to run requeriments with OMR
from sqlmodel import create_engine, Session, text


engine = create_engine("postgresql+psycopg2://postgres:1q2w3e4r5t@:5432/globant_resources")
engine.connect()
session = Session(bind=engine)

query = """
SELECT department, job,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM created_at) = 1 THEN he.id END) as Q1,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM created_at) = 2 THEN he.id END) as Q2,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM created_at) = 3 THEN he.id END) as Q3,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM created_at) = 4 THEN he.id END) as Q4
FROM hired_employees as he
    JOIN departments as d ON (he.department_id=d.id)
    JOIN jobs as j ON (he.job_id=j.id)
    WHERE EXTRACT(YEAR FROM he.created_at) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job;
"""
result = session.exec(text(query)).fetchall()


query2 = """
with deparment_counter as (
    SELECT department_id, department, COUNT(he.id) as hired,
    AVG(COUNT(he.id)) OVER() as hired_mean
    FROM hired_employees as he
    JOIN departments as d ON (he.department_id=d.id)
    WHERE EXTRACT(YEAR FROM he.created_at) = 2021
    GROUP BY department_id, department
)
SELECT department_id, department, hired
FROM deparment_counter
WHERE hired > hired_mean
ORDER BY 3 DESC
"""
result2 = session.exec(text(query2)).fetchall()
# session.rollback()
session.close()
