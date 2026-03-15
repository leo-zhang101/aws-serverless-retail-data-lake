# bronze_to_silver: clean, cast, dedup. Drops bronze metadata cols before writing.
# Returns None on read failure so we can skip that table instead of failing the job.

import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, IntegerType
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME", "BRONZE_BUCKET", "SILVER_BUCKET", "GLUE_DATABASE", "LOAD_DATE"])

spark = SparkSession.builder.getOrCreate()
bronze_bucket = args["BRONZE_BUCKET"]
silver_bucket = args["SILVER_BUCKET"]
load_date_arg = args.get("LOAD_DATE", "TODAY")
load_date = (
    datetime.utcnow().strftime("%Y-%m-%d")
    if (not load_date_arg or str(load_date_arg).strip() == "" or str(load_date_arg) == "TODAY")
    else str(load_date_arg).strip()
)


def read_bronze(table):
    path = f"s3://{bronze_bucket}/{table}/load_date={load_date}/"
    print(f"[bronze_to_silver] {table}: input_path={path}")
    try:
        df = spark.read.parquet(path)
        print(f"[bronze_to_silver] {table}: read={df.count()} rows")
        return df
    except Exception as e:
        print(f"[bronze_to_silver] {table}: read failed - {e}")
        return None


def write_silver(df, table):
    if df is None or df.rdd.isEmpty():
        return
    for c in ["ingestion_ts", "load_date", "source_table"]:
        if c in df.columns:
            df = df.drop(c)
    path = f"s3://{silver_bucket}/{table}/load_date={load_date}/"
    cnt = df.count()
    df.write.mode("overwrite").parquet(path)
    print(f"[bronze_to_silver] {table}: output_path={path}, wrote={cnt} rows")


def safe_col(df, name, default=None):
    return F.col(name) if name in df.columns else (F.lit(default) if default is not None else F.lit(None))


# customer_id, order_id, order_item_id: int in sample. product_id, payment_id, store_id, promotion_id: string.
df = read_bronze("customers")
if df is not None:
    df = df.dropDuplicates(["customer_id"]).filter(F.col("customer_id").isNotNull())
    if "customer_id" in df.columns:
        df = df.withColumn("customer_id", F.col("customer_id").cast(IntegerType())).filter(F.col("customer_id").isNotNull())
    df = df.withColumn("state", F.coalesce(safe_col(df, "state"), F.lit("UNKNOWN")))
    write_silver(df, "customers")

df = read_bronze("orders")
if df is not None:
    df = df.dropDuplicates(["order_id"]).filter(F.col("order_id").isNotNull())
    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType())).filter(F.col("order_id").isNotNull())
    if "customer_id" in df.columns:
        df = df.withColumn("customer_id", F.col("customer_id").cast(IntegerType())).filter(F.col("customer_id").isNotNull())
    if "total_amount_aud" in df.columns:
        df = df.withColumn("total_amount_aud", F.col("total_amount_aud").cast(DoubleType()))
    if "order_date" in df.columns:
        df = df.withColumn("order_date", F.to_date(F.col("order_date")))
    df = df.withColumn("status", F.coalesce(safe_col(df, "status"), F.lit("unknown")))
    write_silver(df, "orders")

df = read_bronze("order_items")
if df is not None:
    df = df.dropDuplicates(["order_item_id"]).filter(F.col("order_item_id").isNotNull())
    if "order_item_id" in df.columns:
        df = df.withColumn("order_item_id", F.col("order_item_id").cast(IntegerType())).filter(F.col("order_item_id").isNotNull())
    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType())).filter(F.col("order_id").isNotNull())
    if "quantity" in df.columns:
        df = df.withColumn("quantity", F.col("quantity").cast(IntegerType()))
    if "unit_price_aud" in df.columns:
        df = df.withColumn("unit_price_aud", F.col("unit_price_aud").cast(DoubleType()))
    if "line_total_aud" in df.columns:
        df = df.withColumn("line_total_aud", F.col("line_total_aud").cast(DoubleType()))
    write_silver(df, "order_items")

df = read_bronze("products")
if df is not None:
    df = df.dropDuplicates(["product_id"]).filter(F.col("product_id").isNotNull())
    if "unit_price_aud" in df.columns:
        df = df.withColumn("unit_price_aud", F.col("unit_price_aud").cast(DoubleType()))
    df = df.withColumn("category", F.coalesce(safe_col(df, "category"), F.lit("Uncategorised")))
    write_silver(df, "products")

df = read_bronze("payments")
if df is not None:
    df = df.dropDuplicates(["payment_id"]).filter(F.col("payment_id").isNotNull())
    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType())).filter(F.col("order_id").isNotNull())
    if "amount_aud" in df.columns:
        df = df.withColumn("amount_aud", F.col("amount_aud").cast(DoubleType()))
    if "payment_date" in df.columns:
        df = df.withColumn("payment_date", F.to_date(F.col("payment_date")))
    write_silver(df, "payments")

df = read_bronze("stores")
if df is not None:
    df = df.dropDuplicates(["store_id"]).filter(F.col("store_id").isNotNull())
    df = df.withColumn("state", F.coalesce(safe_col(df, "state"), F.lit("UNKNOWN")))
    if "opened_at" in df.columns:
        df = df.withColumn("opened_at", F.to_date(F.col("opened_at")))
    write_silver(df, "stores")

df = read_bronze("promotions")
if df is not None:
    df = df.dropDuplicates(["promotion_id"]).filter(F.col("promotion_id").isNotNull())
    if "discount_value_pct" in df.columns:
        df = df.withColumn("discount_value_pct", F.col("discount_value_pct").cast(DoubleType()))
    if "start_date" in df.columns:
        df = df.withColumn("start_date", F.to_date(F.col("start_date")))
    if "end_date" in df.columns:
        df = df.withColumn("end_date", F.to_date(F.col("end_date")))
    write_silver(df, "promotions")

print("[bronze_to_silver] done")
