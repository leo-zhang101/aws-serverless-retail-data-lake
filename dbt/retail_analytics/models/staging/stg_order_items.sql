{{
  config(
    materialized='view',
    tags=['staging', 'order_items']
  )
}}

with source as (
  select * from {{ source('gold', 'order_items') }}
),

renamed as (
  select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price_aud,
    line_total_aud
  from source
  where order_item_id is not null
    and order_id is not null
    and product_id is not null
)

select * from renamed
