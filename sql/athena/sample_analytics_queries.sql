-- Run in Athena, database retail_analytics. Uses MAX(load_date) to pick latest partition.

-- Daily sales
SELECT
  sale_date,
  store_state,
  order_count,
  customer_count,
  total_sales_aud,
  avg_order_value_aud
FROM daily_sales
WHERE load_date = (SELECT MAX(load_date) FROM daily_sales)
ORDER BY sale_date DESC, total_sales_aud DESC;

-- Product performance
SELECT
  product_id,
  product_name,
  category,
  order_count,
  total_quantity_sold,
  total_revenue_aud,
  avg_unit_price_aud
FROM product_performance
WHERE load_date = (SELECT MAX(load_date) FROM product_performance)
ORDER BY total_revenue_aud DESC;

-- Top customers
SELECT
  customer_id,
  customer_name,
  state,
  first_order_date,
  total_orders,
  total_spend_aud,
  avg_order_value_aud
FROM customer_value
WHERE load_date = (SELECT MAX(load_date) FROM customer_value)
ORDER BY total_spend_aud DESC
LIMIT 10;

-- Sales by state
SELECT
  store_state,
  SUM(total_sales_aud) AS total_sales_aud,
  SUM(order_count) AS order_count
FROM daily_sales
WHERE load_date = (SELECT MAX(load_date) FROM daily_sales)
GROUP BY store_state
ORDER BY total_sales_aud DESC;
