-- Number of employees hired for each job and department in 2021 divided by quarter. The
--  table must be ordered alphabetically by department and job

SELECT department, job,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 1 THEN he.id END) as Q1,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 2 THEN he.id END) as Q2,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 3 THEN he.id END) as Q3,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM datetime) = 4 THEN he.id END) as Q4
    FROM hired_employees as he
    JOIN departments as d ON (he.department_id=departments.id)
    JOIN jobs as j ON (he.job_id=jobs.id)
    WHERE EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job

-- List of ids, name and number of employees hired of each department that hired more
--  employees than the mean of employees hired in 2021 for all the departments, ordered
--  by the number of employees hired (descending).

with deparment_counter as (
    SELECT department_id, department, COUNT(he.id) as hired,
    AVG(COUNT(he.id)) OVER() as hired_mean
    FROM hired_employees as he
    JOIN departments as d ON (he.department_id=departments.id)
    WHERE EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY department_id, department
)
SELECT department_id, department, hired
FROM deparment_counter
WHERE hired > hired_mean
ORDER BY 3 DESC