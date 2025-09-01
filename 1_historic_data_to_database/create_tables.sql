
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY NOT NULL ,
    job VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE departments (
    id SERIAL PRIMARY KEY NOT NULL ,
    department VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE hired_employees (
    id SERIAL PRIMARY KEY NOT NULL ,
    name VARCHAR(100) NOT NULL,
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    department_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);