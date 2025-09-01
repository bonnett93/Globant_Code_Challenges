### Migration Steps

We assume we transfer old db daba to csv and store in gcp cloud storage.

We select postgres sql with cloud sql as new db

Optional: Confirm user and project
- gcloud auth list
- gcloud config list project
- gcloud config set project project_id

---

1. **Create Cloud SQL instance with postgresql:** Use gcp shell
    
        gcloud sql instances create globant-resources \
            --database-version=POSTGRES_13 --cpu=2 --memory=8GiB \
            --region="europe-west1" --root-password=Passw0rd

2. **ENV Variables**: Create an environment variable with the Cloud Shell IP address.

    Allowlist the Cloud Shell instance for management access to your SQL instance

         export ADDRESS=$(curl -s http://ipecho.net/plain)/32
         
         gcloud sql instances patch globant-resources --authorized-networks $ADDRESS

3. **Create DB and Tables**: In the GCP console go to sql, select globant-resources instance 
   - Create a new DB: Go to database, then new, and call it **"human_resources"**
   - To create table: Go to Overview, then import, In Browse select local machine and upload create_tables.sql file,
   select SQL as File format, globant-resources as destination

4. **Import Data**:
   - Again in Overview, then import, this time CSV as File format.
   - Browse the storage bucket the files are, select one, link with it table
   - repeat for other 2 files
