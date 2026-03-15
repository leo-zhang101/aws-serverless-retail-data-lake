# raw_to_bronze: CSV → Parquet. Adds ingestion_ts, load_date, source_table for lineage.
# Skips tables that fail to read (e.g. missing partition) so other tables still process.

import sys
from datetime import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME", "RAW_BUCKET", "BRONZE_BUCKET", "GLUE_DATABASE", "LOAD_DATE"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

raw_bucket = args["RAW_BUCKET"]
bronze_bucket = args["BRONZE_BUCKET"]
load_date_arg = args.get("LOAD_DATE", "TODAY")
load_date = (
    datetime.utcnow().strftime("%Y-%m-%d")
    if (not load_date_arg or str(load_date_arg).strip() == "" or str(load_date_arg) == "TODAY")
    else str(load_date_arg).strip()
)
ingestion_ts = datetime.utcnow().isoformat() + "Z"

tables = ["customers", "orders", "order_items", "products", "payments", "stores", "promotions"]

for table in tables:
    raw_path = f"s3://{raw_bucket}/{table}/load_date={load_date}/"
    bronze_path = f"s3://{bronze_bucket}/{table}/load_date={load_date}/"
    print(f"[raw_to_bronze] {table}: input_path={raw_path}")

    try:
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(raw_path)
        read_count = df.count()
        # Overwrite: we're doing full refresh per load_date. Append would need dedup logic.
        df = df.withColumn("ingestion_ts", F.lit(ingestion_ts)).withColumn("load_date", F.lit(load_date)).withColumn("source_table", F.lit(table))
        df.write.mode("overwrite").parquet(bronze_path)
        print(f"[raw_to_bronze] {table}: read={read_count}, wrote={read_count}, output_path={bronze_path}")
    except Exception as e:
        print(f"[raw_to_bronze] {table}: table={table}, path={raw_path}, error={e}")

job.commit()
