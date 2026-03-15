{{
  config(
    materialized='view',
    tags=['intermediate', 'orders']
  )
}}

with orders as (
  select * from {{ ref('stg_orders') }}
),
customers as (
  select * from {{ ref('stg_customers') }}
),
stores as (
  select * from {{ ref('stg_stores') }}
),
promotions as (
  select * from {{ ref('stg_promotions') }}
)

select
  o.order_id,
  o.customer_id,
  c.first_name || ' ' || c.last_name as customer_name,
  c.state as customer_state,
  o.store_id,
  s.store_name,
  s.state as store_state,
  o.order_date,
  o.total_amount_aud,
  o.status,
  o.promotion_id,
  p.promotion_name,
  p.discount_value_pct
from orders o
left join customers c on o.customer_id = c.customer_id
left join stores s on o.store_id = s.store_id
left join promotions p on o.promotion_id = p.promotion_id
