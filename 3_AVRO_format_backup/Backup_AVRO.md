### Backup In AVRO

We select postgres sql with cloud sql as a db and us-west1 as the gpc region

Optional: Confirm user and project
- gcloud auth list
- gcloud config list project
---
The next steps are example to create backup process for Jobs table

**1. Create Table backup main**
the file main_backup_jobs.py is the main to create a Cloud Cron Job, this script:
- Reads cloudSQL with postgreSQL
- Converter files to AVRO
- Save it in a gcp bucket

**2. Create GCP Schedule Job**
.env.yaml file is empty, but you can put ENV vars there

    gcloud auth login

    gcloud pubsub topics create backup_avro_jobstable_topic --project={PROJECT_ID}

    gcloud functions deploy backup_avro_db --env-vars-file .env.yaml --region=us-west1 --entry-point main_backup_jobs --runtime python313 --memory 1024MB --trigger-resource backup_avro_jobstable_topic--trigger-event google.pubsub.topic.publish --timeout 540s --no-gen2

    gcloud scheduler jobs create pubsub avro_backup_daily_job --location=us-east1 --schedule "0 1 * * *" --topic backup_avro_jobstable_topic--time-zone="America/Bogota" --message-body "this job runs once a day"
