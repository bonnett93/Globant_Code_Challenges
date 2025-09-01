import psycopg2
from google.cloud import storage
from fastavro import reader
from psycopg2 import extras
import io


PROJECT_ID = ""
GCS_BUCKET_NAME = "nombre_de_tu_bucket"
GCS_FILE_NAME = "nombre_de_tu_archivo.avro"
DB_NAME = "nombre_de_tu_bd"
DB_USER = "usuario_bd"
DB_PASSWORD = "tu_password"
f"/cloudsql/{PROJECT_ID}:us-west1:globant-resources"
CLOUD_SQL_HOST = "/cloudsql/tu_proyecto:tu_region:tu_instancia_cloud_sql"
TABLE_NAME = "jobs"

try:
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_FILE_NAME)

    avro_buffer = io.BytesIO()
    blob.download_to_file(avro_buffer)
    avro_buffer.seek(0)
    print(f"File '{GCS_FILE_NAME}' download success!.")

except Exception as error:
    print("Cloud Storage: Download file Error:", error)
    exit()


records = []
try:

    avro_reader = reader(avro_buffer)
    for record in avro_reader:
        records.append(record)
    if not records:
        print("Empty file. Exit...")
        exit()

except Exception as error:
    print("Read Avro: Error:", error)
    exit()


try:
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=CLOUD_SQL_HOST
    )
    cursor = conn.cursor()

    columns = records[0].keys()
    columns_str = ', '.join(columns)
    values_def = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({values_def})"


    data_to_insert = [tuple(record.values()) for record in records]
    extras.execute_batch(cursor, insert_query, data_to_insert)

    conn.commit()
    print(f"Upload {cursor.rowcount} lines in '{TABLE_NAME}' PostgreSQL table.")

except (Exception, psycopg2.Error) as error:
    print("Conn: Error:", error)
    conn.rollback()  # Revierte cualquier cambio en caso de error

finally:
    if conn:
        cursor.close()
        conn.close()
