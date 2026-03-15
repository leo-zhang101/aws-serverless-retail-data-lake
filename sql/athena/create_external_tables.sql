-- External tables over gold. Replace REPLACE_GOLD_BUCKET before running.
CREATE EXTERNAL TABLE IF NOT EXISTS daily_sales (
  sale_date DATE,
  store_state STRING,
  order_count BIGINT,
  customer_count BIGINT,
  total_sales_aud DOUBLE,
  avg_order_value_aud DOUBLE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/daily_sales/';

CREATE EXTERNAL TABLE IF NOT EXISTS product_performance (
  product_id STRING,
  product_name STRING,
  category STRING,
  order_count BIGINT,
  total_quantity_sold BIGINT,
  total_revenue_aud DOUBLE,
  avg_unit_price_aud DOUBLE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/product_performance/';

CREATE EXTERNAL TABLE IF NOT EXISTS customer_value (
  customer_id INT,
  customer_name STRING,
  state STRING,
  first_order_date DATE,
  total_orders BIGINT,
  total_spend_aud DOUBLE,
  avg_order_value_aud DOUBLE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/customer_value/';

CREATE EXTERNAL TABLE IF NOT EXISTS customers (
  customer_id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  state STRING,
  created_at STRING
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/customers/';

CREATE EXTERNAL TABLE IF NOT EXISTS orders (
  order_id INT,
  customer_id INT,
  store_id STRING,
  order_date DATE,
  total_amount_aud DOUBLE,
  status STRING,
  promotion_id STRING
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/orders/';

CREATE EXTERNAL TABLE IF NOT EXISTS order_items (
  order_item_id INT,
  order_id INT,
  product_id STRING,
  quantity INT,
  unit_price_aud DOUBLE,
  line_total_aud DOUBLE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/order_items/';

CREATE EXTERNAL TABLE IF NOT EXISTS products (
  product_id STRING,
  product_name STRING,
  category STRING,
  unit_price_aud DOUBLE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/products/';

CREATE EXTERNAL TABLE IF NOT EXISTS payments (
  payment_id STRING,
  order_id INT,
  amount_aud DOUBLE,
  payment_method STRING,
  payment_date DATE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/payments/';

CREATE EXTERNAL TABLE IF NOT EXISTS stores (
  store_id STRING,
  store_name STRING,
  state STRING,
  city STRING,
  opened_at DATE
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/stores/';

CREATE EXTERNAL TABLE IF NOT EXISTS promotions (
  promotion_id STRING,
  promotion_name STRING,
  discount_type STRING,
  discount_value_pct DOUBLE,
  start_date DATE,
  end_date DATE,
  active STRING
)
PARTITIONED BY (load_date STRING)
STORED AS PARQUET
LOCATION 's3://retail-analytics-dev-gold-3f59eff9/promotions/';
-- Add partitions (run after Glue job, replace LOAD_DATE and GOLD_BUCKET)
-- MSCK REPAIR TABLE daily_sales;
-- MSCK REPAIR TABLE product_performance;
-- MSCK REPAIR TABLE customer_value;
-- MSCK REPAIR TABLE customers;
-- MSCK REPAIR TABLE orders;
-- MSCK REPAIR TABLE order_items;
-- MSCK REPAIR TABLE products;
-- MSCK REPAIR TABLE payments;
-- MSCK REPAIR TABLE stores;
-- MSCK REPAIR TABLE promotions;
