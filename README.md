# Proposal for Coding Challenge
### Globant

This repository contains the **Proof of Concept (PoC)** for solving **Challenge #1** of the Globant Coding Challenge.

---
## Challenge #1

### Structure
This is the structure to solve the requirements

**1_historic_data_to_database** Contains the solution for:  Move historic data from files in CSV format to the new database.

**app** Contains the solution for: Create a Rest API service to receive new data.
As the request say the api is just to receive new data.
So allow methods: POST

to use CloudSQL: Use one of this options as DATABASE_URL env var

        postgresql://usuario:password@cloud-sql_ip:db_port/db_name
        mysql+pymysql://user:password@cloud-sql_ip/db_name

postgresql conventional port is 5432, and requires install psycopg or psycopg2

**3_AVRO_format_backup** Contains the solution for:  Create a feature to backup for each table and save it in the file system in AVRO format.

**4_restore_table_from_AVRO_backup** Contains the solution for: Create a feature to restore a certain table with its backup.


## Requirements
All dependencies are listed in `requirements.txt`.

## Deploy app
**dev:**

powerShell

    $env:ENVIRONMENT="DEV"
    uvicorn app.main:app --reload

ubuntu

    export ENVIRONMENT="DEV"
    uvicorn app.main:app --reload