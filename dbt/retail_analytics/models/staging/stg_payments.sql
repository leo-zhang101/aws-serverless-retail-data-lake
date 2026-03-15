{{
  config(
    materialized='view',
    tags=['staging', 'payments']
  )
}}

with source as (
  select * from {{ source('gold', 'payments') }}
),

renamed as (
  select
    payment_id,
    order_id,
    amount_aud,
    payment_method,
    payment_date::date as payment_date
  from source
  where payment_id is not null
    and order_id is not null
)

select * from renamed
