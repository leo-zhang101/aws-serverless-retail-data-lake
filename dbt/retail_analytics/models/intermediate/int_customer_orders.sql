{{
  config(
    materialized='view',
    tags=['intermediate', 'customers']
  )
}}

with orders as (
  select * from {{ ref('stg_orders') }}
),
payments as (
  select * from {{ ref('stg_payments') }}
)

select
  o.customer_id,
  o.order_id,
  o.order_date,
  o.total_amount_aud as order_amount_aud,
  p.amount_aud as payment_amount_aud,
  o.status
from orders o
left join payments p on o.order_id = p.order_id
