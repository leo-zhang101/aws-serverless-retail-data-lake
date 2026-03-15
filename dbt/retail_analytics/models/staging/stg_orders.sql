{{
  config(
    materialized='view',
    tags=['staging', 'orders']
  )
}}

with source as (
  select * from {{ source('gold', 'orders') }}
),

renamed as (
  select
    order_id,
    customer_id,
    store_id,
    order_date::date as order_date,
    total_amount_aud,
    status,
    promotion_id,
    coalesce(status, 'unknown') as status_normalised
  from source
  where order_id is not null
    and order_date is not null
)

select * from renamed
