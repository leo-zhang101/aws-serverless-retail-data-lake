"""
Glue Job: bronze_to_silver
Reads Parquet from bronze, applies cleaning, basic data quality checks,
type casting and standardisation, then writes to silver.

Supports --LOAD_DATE; if empty or TODAY, uses current date.
"""

import sys
from datetime import datetime

from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, IntegerType


args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "BRONZE_BUCKET", "SILVER_BUCKET", "GLUE_DATABASE", "LOAD_DATE"],
)

spark = SparkSession.builder.getOrCreate()

bronze_bucket = args["BRONZE_BUCKET"]
silver_bucket = args["SILVER_BUCKET"]

load_date_arg = args.get("LOAD_DATE", "TODAY")
load_date = (
    datetime.utcnow().strftime("%Y-%m-%d")
    if (not load_date_arg or str(load_date_arg).strip() == "" or str(load_date_arg) == "TODAY")
    else str(load_date_arg).strip()
)


def read_bronze(table: str):
    """Read a bronze parquet table for the given load date."""
    path = f"s3://{bronze_bucket}/{table}/load_date={load_date}/"
    print(f"[bronze_to_silver] {table}: input_path={path}")
    try:
        df = spark.read.parquet(path)
        count = df.count()
        print(f"[bronze_to_silver] {table}: read_count={count}")
        return df
    except Exception as e:
        print(f"[bronze_to_silver] {table}: read_failed={e}")
        return None


def write_silver(df, table: str):
    """Write silver parquet output for the given table and load date."""
    if df is None or df.rdd.isEmpty():
        print(f"[bronze_to_silver] {table}: no_data_to_write")
        return

    path = f"s3://{silver_bucket}/{table}/load_date={load_date}/"
    write_count = df.count()
    df.write.mode("overwrite").parquet(path)
    print(f"[bronze_to_silver] {table}: output_path={path}, write_count={write_count}")


def safe_col(df, name: str, default=None):
    """Return a column if present, otherwise a literal default/null."""
    if name in df.columns:
        return F.col(name)
    return F.lit(default) if default is not None else F.lit(None)


# ----------------------------
# Data quality helper functions
# ----------------------------

def validate_customers(df):
    """
    Customer rules:
    - customer_id must not be null
    - customer_id should be unique
    """
    if "customer_id" in df.columns:
        df = df.filter(F.col("customer_id").isNotNull())
        df = df.dropDuplicates(["customer_id"])
    return df


def validate_orders(df):
    """
    Order rules:
    - order_id must not be null
    - customer_id must not be null
    - total_amount_aud must be > 0
    - order_id should be unique
    """
    if "order_id" in df.columns:
        df = df.filter(F.col("order_id").isNotNull())
        df = df.dropDuplicates(["order_id"])

    if "customer_id" in df.columns:
        df = df.filter(F.col("customer_id").isNotNull())

    if "total_amount_aud" in df.columns:
        df = df.filter(F.col("total_amount_aud") > 0)

    return df


def validate_order_items(df):
    """
    Order item rules:
    - order_item_id must not be null
    - quantity must be > 0
    - line_total_aud must be > 0
    """
    if "order_item_id" in df.columns:
        df = df.filter(F.col("order_item_id").isNotNull())
        df = df.dropDuplicates(["order_item_id"])

    if "quantity" in df.columns:
        df = df.filter(F.col("quantity") > 0)

    if "line_total_aud" in df.columns:
        df = df.filter(F.col("line_total_aud") > 0)

    return df


def validate_payments(df):
    """
    Payment rules:
    - payment_id must not be null
    - amount_aud must be > 0
    """
    if "payment_id" in df.columns:
        df = df.filter(F.col("payment_id").isNotNull())
        df = df.dropDuplicates(["payment_id"])

    if "amount_aud" in df.columns:
        df = df.filter(F.col("amount_aud") > 0)

    return df


def validate_products(df):
    """
    Product rules:
    - product_id must not be null
    - unit_price_aud must be > 0 if present
    """
    if "product_id" in df.columns:
        df = df.filter(F.col("product_id").isNotNull())
        df = df.dropDuplicates(["product_id"])

    if "unit_price_aud" in df.columns:
        df = df.filter(F.col("unit_price_aud") > 0)

    return df


def validate_stores(df):
    """
    Store rules:
    - store_id must not be null
    """
    if "store_id" in df.columns:
        df = df.filter(F.col("store_id").isNotNull())
        df = df.dropDuplicates(["store_id"])
    return df


def validate_promotions(df):
    """
    Promotion rules:
    - promotion_id must not be null
    """
    if "promotion_id" in df.columns:
        df = df.filter(F.col("promotion_id").isNotNull())
        df = df.dropDuplicates(["promotion_id"])
    return df


# ----------------------------
# customers
# ----------------------------
df = read_bronze("customers")
if df is not None:
    if "customer_id" in df.columns:
        df = df.withColumn("customer_id", F.col("customer_id").cast(IntegerType()))

    df = df.withColumn("state", F.coalesce(safe_col(df, "state"), F.lit("UNKNOWN")))

    df = validate_customers(df)
    write_silver(df, "customers")


# ----------------------------
# orders
# ----------------------------
df = read_bronze("orders")
if df is not None:
    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType()))

    if "customer_id" in df.columns:
        df = df.withColumn("customer_id", F.col("customer_id").cast(IntegerType()))

    if "total_amount_aud" in df.columns:
        df = df.withColumn("total_amount_aud", F.col("total_amount_aud").cast(DoubleType()))

    if "order_date" in df.columns:
        df = df.withColumn("order_date", F.to_date(F.col("order_date")))

    df = df.withColumn("status", F.coalesce(safe_col(df, "status"), F.lit("unknown")))

    df = validate_orders(df)
    write_silver(df, "orders")


# ----------------------------
# order_items
# ----------------------------
df = read_bronze("order_items")
if df is not None:
    if "order_item_id" in df.columns:
        df = df.withColumn("order_item_id", F.col("order_item_id").cast(IntegerType()))

    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType()))

    if "quantity" in df.columns:
        df = df.withColumn("quantity", F.col("quantity").cast(IntegerType()))

    if "unit_price_aud" in df.columns:
        df = df.withColumn("unit_price_aud", F.col("unit_price_aud").cast(DoubleType()))

    if "line_total_aud" in df.columns:
        df = df.withColumn("line_total_aud", F.col("line_total_aud").cast(DoubleType()))

    df = validate_order_items(df)
    write_silver(df, "order_items")


# ----------------------------
# products
# ----------------------------
df = read_bronze("products")
if df is not None:
    if "unit_price_aud" in df.columns:
        df = df.withColumn("unit_price_aud", F.col("unit_price_aud").cast(DoubleType()))

    df = df.withColumn("category", F.coalesce(safe_col(df, "category"), F.lit("Uncategorised")))

    df = validate_products(df)
    write_silver(df, "products")


# ----------------------------
# payments
# ----------------------------
df = read_bronze("payments")
if df is not None:
    if "order_id" in df.columns:
        df = df.withColumn("order_id", F.col("order_id").cast(IntegerType()))

    if "amount_aud" in df.columns:
        df = df.withColumn("amount_aud", F.col("amount_aud").cast(DoubleType()))

    if "payment_date" in df.columns:
        df = df.withColumn("payment_date", F.to_date(F.col("payment_date")))

    df = validate_payments(df)
    write_silver(df, "payments")


# ----------------------------
# stores
# ----------------------------
df = read_bronze("stores")
if df is not None:
    df = df.withColumn("state", F.coalesce(safe_col(df, "state"), F.lit("UNKNOWN")))

    if "opened_at" in df.columns:
        df = df.withColumn("opened_at", F.to_date(F.col("opened_at")))

    df = validate_stores(df)
    write_silver(df, "stores")


# ----------------------------
# promotions
# ----------------------------
df = read_bronze("promotions")
if df is not None:
    if "discount_value_pct" in df.columns:
        df = df.withColumn("discount_value_pct", F.col("discount_value_pct").cast(DoubleType()))

    if "start_date" in df.columns:
        df = df.withColumn("start_date", F.to_date(F.col("start_date")))

    if "end_date" in df.columns:
        df = df.withColumn("end_date", F.to_date(F.col("end_date")))

    df = validate_promotions(df)
    write_silver(df, "promotions")


print("[bronze_to_silver] completed")
