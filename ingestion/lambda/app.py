# Uploads sample_data/*.csv to raw S3. Path: {table}/load_date=YYYY-MM-DD/{table}.csv
# Event can pass load_date; otherwise uses today. Zip includes sample_data/ so Lambda has the files.

import os
import json
from datetime import datetime, timezone
import boto3

RAW_BUCKET = os.environ.get("RAW_BUCKET", "")
SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sample_data")

TABLES = ["customers", "orders", "order_items", "products", "payments", "stores", "promotions"]


def lambda_handler(event, context):
    load_date = event.get("load_date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    load_date = str(load_date).strip()

    if not RAW_BUCKET:
        return {"statusCode": 500, "body": json.dumps({"error": "RAW_BUCKET not set"})}

    s3 = boto3.client("s3")
    uploaded = []

    for table in TABLES:
        filename = f"{table}.csv"
        local_path = os.path.join(SAMPLE_DATA_DIR, filename)

        if not os.path.exists(local_path):
            print(f"[ingestion] skip {table}: not found {local_path}")
            continue

        s3_key = f"{table}/load_date={load_date}/{filename}"
        try:
            s3.upload_file(local_path, RAW_BUCKET, s3_key)
            uploaded.append({"table": table, "key": s3_key})
            print(f"[ingestion] {table} -> s3://{RAW_BUCKET}/{s3_key}")
        except Exception as e:
            print(f"[ingestion] {table} failed: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps({"load_date": load_date, "uploaded_count": len(uploaded), "uploaded": uploaded}),
    }
