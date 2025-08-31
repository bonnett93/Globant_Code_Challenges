# Proposal for Coding Challenge
### Globant

This repository contains the **Proof of Concept (PoC)** for solving **Challenge #1** of the Globant Coding Challenge.

---
## Challenge #1

### Structure
This is the structure to solve the requirements

**1_historic_data_to_database** Contains the solution for:  Move historic data from files in CSV format to the new database.

**app** Contains the solution for: Create a Rest API service to receive new data.

**3_AVRO_format_backup** Contains the solution for:  Create a feature to backup for each table and save it in the file system in AVRO format.

**4_restore_table_from_AVRO_backup** Contains the solution for: Create a feature to restore a certain table with its backup.


## Requirements
All dependencies are listed in `requirements.txt`.

## Deploy
uvicorn app.main:app --reload