{{
  config(
    materialized='table',
    tags=['marts', 'daily_sales']
  )
}}

with orders as (
  select * from {{ ref('int_orders_enriched') }}
)

select
  order_date as sale_date,
  coalesce(store_state, 'Unknown') as store_state,
  count(distinct order_id) as order_count,
  count(distinct customer_id) as customer_count,
  sum(total_amount_aud) as total_sales_aud,
  round(avg(total_amount_aud), 2) as avg_order_value_aud
from orders
where status = 'completed'
group by order_date, coalesce(store_state, 'Unknown')
order by sale_date desc, store_state
