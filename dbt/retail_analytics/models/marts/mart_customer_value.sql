{{
  config(
    materialized='table',
    tags=['marts', 'customer_value']
  )
}}

with customer_orders as (
  select * from {{ ref('int_customer_orders') }}
),
customers as (
  select * from {{ ref('stg_customers') }}
)

select
  co.customer_id,
  c.first_name || ' ' || c.last_name as customer_name,
  c.state,
  c.created_at as first_order_date,
  count(distinct co.order_id) as total_orders,
  sum(co.order_amount_aud) as total_spend_aud,
  round(avg(co.order_amount_aud), 2) as avg_order_value_aud
from customer_orders co
left join customers c on co.customer_id = c.customer_id
where co.status = 'completed'
group by co.customer_id, c.first_name, c.last_name, c.state, c.created_at
order by total_spend_aud desc
