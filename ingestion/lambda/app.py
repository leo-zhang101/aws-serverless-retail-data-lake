import os
import json
import logging
from datetime import datetime
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

RAW_BUCKET = os.environ.get("RAW_BUCKET", "")
SAMPLE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "sample_data"
)

TABLES = [
    "customers",
    "orders",
    "order_items",
    "products",
    "payments",
    "stores",
    "promotions",
]


def lambda_handler(event, context):
    logger.info("Lambda ingestion started")
    logger.info(f"Received event: {event}")

    load_date = event.get("load_date") or datetime.utcnow().strftime("%Y-%m-%d")
    load_date = str(load_date).strip()

    if not RAW_BUCKET:
        logger.error("RAW_BUCKET not set")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "RAW_BUCKET not set"})
        }

    s3 = boto3.client("s3")
    uploaded = []

    for table in TABLES:
        filename = f"{table}.csv"
        local_path = os.path.join(SAMPLE_DATA_DIR, filename)

        if not os.path.exists(local_path):
            logger.warning(f"[ingestion] skip {table}: file not found {local_path}")
            continue

        s3_key = f"{table}/load_date={load_date}/{filename}"

        try:
            s3.upload_file(local_path, RAW_BUCKET, s3_key)
            size = os.path.getsize(local_path)
            logger.info(f"[ingestion] uploaded {table}: s3://{RAW_BUCKET}/{s3_key} ({size} bytes)")
            uploaded.append({
                "table": table,
                "key": s3_key,
                "path": f"s3://{RAW_BUCKET}/{s3_key}"
            })
        except Exception as e:
            logger.error(f"[ingestion] failed {table}: {e}")

    logger.info(f"Lambda ingestion completed. Uploaded {len(uploaded)} files for load_date={load_date}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "load_date": load_date,
            "uploaded_count": len(uploaded),
            "uploaded": uploaded,
        }),
    }
