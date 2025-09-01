import psycopg2
from google.cloud import storage
from fastavro import writer, parse_schema
import io


DB_NAME = "nombre_de_tu_bd"
DB_USER = "usuario_bd"
DB_PASSWORD = "tu_password"
PROJECT_ID = "nombre_de_tu_bd"
CLOUD_SQL_HOST = f"/cloudsql/{PROJECT_ID}:us-west1:globant_resources"
TABLE_NAME = "jobs"
GCS_BUCKET_NAME = "human_resources_raw_backup"
GCS_FILE_NAME = "backup_jobs.avro"

avro_schema = {
    "type": "record",
    "name": "TableName",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "job", "type": "string"},
    ]
}

# DB Conn and Extract
records = []
try:
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=CLOUD_SQL_HOST
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    rows = cursor.fetchall()

    for row in rows:
        record = {
            "column1": row[0],
            "column2": row[1],
        }
        records.append(record)

    cursor.close()
    conn.close()
    print("PostgreSQL read OK.")

except (Exception, psycopg2.Error) as error:
    print("PostgreSQL connection error:", error)
    exit()

# AVRO file converter
parsed_schema = parse_schema(avro_schema)
buffer = io.BytesIO()
writer(buffer, parsed_schema, records)
buffer.seek(0) # Go to buffer init
print(f"Converted {len(records)} lines to avro.")


try:
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_FILE_NAME)
    blob.upload_from_file(buffer, content_type='application/octet-stream') # Generic file type
    print(f"Cloud Storage: File '{GCS_FILE_NAME}' upload with success in'{GCS_BUCKET_NAME}' bucket.")

except Exception as error:
    print("Cloud Storage: Upload file Error:", error)