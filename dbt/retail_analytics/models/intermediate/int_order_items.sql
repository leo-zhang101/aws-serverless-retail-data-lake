{{
  config(
    materialized='view',
    tags=['intermediate', 'order_items']
  )
}}

with order_items as (
  select * from {{ ref('stg_order_items') }}
),
products as (
  select * from {{ ref('stg_products') }}
),
orders as (
  select * from {{ ref('stg_orders') }}
)

select
  oi.order_item_id,
  oi.order_id,
  oi.product_id,
  p.product_name,
  p.category,
  oi.quantity,
  oi.unit_price_aud,
  oi.line_total_aud,
  o.order_date
from order_items oi
left join products p on oi.product_id = p.product_id
left join orders o on oi.order_id = o.order_id
