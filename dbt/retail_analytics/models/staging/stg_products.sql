{{
  config(
    materialized='view',
    tags=['staging', 'products']
  )
}}

with source as (
  select * from {{ source('gold', 'products') }}
),

renamed as (
  select
    product_id,
    product_name,
    category,
    unit_price_aud,
    coalesce(category, 'Uncategorised') as category_normalised
  from source
  where product_id is not null
)

select * from renamed
