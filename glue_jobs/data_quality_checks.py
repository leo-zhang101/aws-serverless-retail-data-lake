from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def validate_orders(df: DataFrame) -> DataFrame:
    """
    Basic data quality checks for orders.
    Rules:
    - order_id must not be null
    - customer_id must not be null
    - total_amount_aud must be greater than 0
    - order_id must be unique
    """
    df = df.filter(F.col("order_id").isNotNull())
    df = df.filter(F.col("customer_id").isNotNull())
    df = df.filter(F.col("total_amount_aud") > 0)
    df = df.dropDuplicates(["order_id"])
    return df


def validate_order_items(df: DataFrame) -> DataFrame:
    """
    Basic data quality checks for order items.
    Rules:
    - order_item_id must not be null
    - quantity must be greater than 0
    - line_total_aud must be greater than 0
    """
    df = df.filter(F.col("order_item_id").isNotNull())
    df = df.filter(F.col("quantity") > 0)
    df = df.filter(F.col("line_total_aud") > 0)
    return df


def validate_customers(df: DataFrame) -> DataFrame:
    """
    Basic data quality checks for customers.
    Rules:
    - customer_id must not be null
    """
    df = df.filter(F.col("customer_id").isNotNull())
    return df
