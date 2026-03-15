{{
  config(
    materialized='table',
    tags=['marts', 'product_performance']
  )
}}

with order_items as (
  select * from {{ ref('int_order_items') }}
)

select
  product_id,
  product_name,
  category,
  count(distinct order_id) as order_count,
  sum(quantity) as total_quantity_sold,
  sum(line_total_aud) as total_revenue_aud,
  round(avg(unit_price_aud), 2) as avg_unit_price_aud
from order_items
group by product_id, product_name, category
order by total_revenue_aud desc
