# silver_to_gold: build analytics tables + pass-through dims.
# Left joins: orders may have no store; we still want them in daily_sales with store_state=Unknown.

import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME", "SILVER_BUCKET", "GOLD_BUCKET", "GLUE_DATABASE", "LOAD_DATE"])

spark = SparkSession.builder.getOrCreate()
silver_bucket = args["SILVER_BUCKET"]
gold_bucket = args["GOLD_BUCKET"]
load_date_arg = args.get("LOAD_DATE", "TODAY")
load_date = (
    datetime.utcnow().strftime("%Y-%m-%d")
    if (not load_date_arg or str(load_date_arg).strip() == "" or str(load_date_arg) == "TODAY")
    else str(load_date_arg).strip()
)


def read_silver(table):
    path = f"s3://{silver_bucket}/{table}/load_date={load_date}/"
    print(f"[silver_to_gold] {table}: input_path={path}")
    try:
        df = spark.read.parquet(path)
        print(f"[silver_to_gold] {table}: read={df.count()} rows")
        return df
    except Exception as e:
        print(f"[silver_to_gold] {table}: read failed - {e}")
        return None


def write_gold(df, table):
    if df is None or df.rdd.isEmpty():
        return
    path = f"s3://{gold_bucket}/{table}/load_date={load_date}/"
    cnt = df.count()
    df.write.mode("overwrite").parquet(path)
    print(f"[silver_to_gold] {table}: output_path={path}, wrote={cnt} rows")


orders = read_silver("orders")
order_items = read_silver("order_items")
customers = read_silver("customers")
products = read_silver("products")
stores = read_silver("stores")

if orders is None:
    print("[silver_to_gold] no orders, skipping analytics")
else:
    if stores is not None:
        orders_with_store = orders.join(
            stores.select("store_id", F.col("state").alias("store_state")), "store_id", "left"
        ).withColumn("store_state", F.coalesce(F.col("store_state"), F.lit("Unknown")))
    else:
        orders_with_store = orders.withColumn("store_state", F.lit("Unknown"))

    completed = orders_with_store.filter(F.col("status") == "completed") if "status" in orders_with_store.columns else orders_with_store

    daily_sales = completed.groupBy(
        F.col("order_date").alias("sale_date"),
        F.coalesce(F.col("store_state"), F.lit("Unknown")).alias("store_state"),
    ).agg(
        F.countDistinct("order_id").alias("order_count"),
        F.countDistinct("customer_id").alias("customer_count"),
        F.sum("total_amount_aud").alias("total_sales_aud"),
        F.round(F.avg("total_amount_aud"), 2).alias("avg_order_value_aud"),
    )
    write_gold(daily_sales, "daily_sales")

if order_items is not None and products is not None:
    oi = order_items.alias("oi")
    p = products.select(
        F.col("product_id").alias("product_id_dim"),
        F.col("product_name"),
        F.col("category")
    ).alias("p")

    oi_join = oi.join(
        p,
        F.col("oi.product_id") == F.col("p.product_id_dim"),
        "left"
    )

    product_perf = oi_join.groupBy(
        F.coalesce(F.col("oi.product_id"), F.lit("unknown")).alias("product_id"),
        F.coalesce(F.col("p.product_name"), F.lit("Unknown")).alias("product_name"),
        F.coalesce(F.col("p.category"), F.lit("Uncategorised")).alias("category")
    ).agg(
        F.countDistinct(F.col("oi.order_id")).alias("order_count"),
        F.sum(F.col("oi.quantity")).alias("total_quantity_sold"),
        F.sum(F.col("oi.line_total_aud")).alias("total_revenue_aud"),
        F.round(F.avg(F.col("oi.unit_price_aud")), 2).alias("avg_unit_price_aud")
    )

    write_gold(product_perf, "product_performance")

    if customers is not None:
        completed_orders = orders.filter(F.col("status") == "completed") if "status" in orders.columns else orders
        cust_agg = completed_orders.groupBy("customer_id").agg(
            F.count("order_id").alias("total_orders"),
            F.sum("total_amount_aud").alias("total_spend_aud"),
            F.round(F.avg("total_amount_aud"), 2).alias("avg_order_value_aud"),
            F.min("order_date").alias("first_order_date"),
        )
        fn = F.coalesce(customers.first_name, F.lit("")) if "first_name" in customers.columns else F.lit("")
        ln = F.coalesce(customers.last_name, F.lit("")) if "last_name" in customers.columns else F.lit("")
        customer_value = cust_agg.join(customers, cust_agg.customer_id == customers.customer_id, "left").select(
            cust_agg.customer_id,
            (fn + F.lit(" ") + ln).alias("customer_name"),
            F.coalesce(customers.state, F.lit("Unknown")).alias("state"),
            cust_agg.first_order_date,
            cust_agg.total_orders,
            cust_agg.total_spend_aud,
            cust_agg.avg_order_value_aud,
        )
        write_gold(customer_value, "customer_value")

for table in ["customers", "orders", "order_items", "products", "payments", "stores", "promotions"]:
    df = read_silver(table)
    if df is not None:
        write_gold(df, table)

print("[silver_to_gold] done")
