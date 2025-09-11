# Proposal for Coding Challenge
### Globant

This repository contains the **Proof of Concept (PoC)** for solving **Challenge #1** of the Globant Coding Challenge.

---
## Challenge #1

---

## 2. Create a Rest API service to receive new data.

As the request say the api is just to receive new data.
So allow methods: POST

to use CloudSQL: Use one of this options as DATABASE_URL env var

        postgresql+psycopg2://usuario:password@cloud-sql_ip:db_port/db_name
        mysql+pymysql://user:password@cloud-sql_ip/db_name

postgresql conventional port is 5432, and requires install psycopg or psycopg2

## Requirements
All dependencies are listed in `requirements.txt`.

### Deploy app
**dev:**

powerShell

    $env:ENVIRONMENT="DEV"
    uvicorn app.main:app --reload

ubuntu

    export ENVIRONMENT="DEV"
    uvicorn app.main:app --reload