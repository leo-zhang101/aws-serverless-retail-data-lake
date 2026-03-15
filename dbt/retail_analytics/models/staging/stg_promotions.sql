{{
  config(
    materialized='view',
    tags=['staging', 'promotions']
  )
}}

with source as (
  select * from {{ source('gold', 'promotions') }}
),

renamed as (
  select
    promotion_id,
    promotion_name,
    discount_type,
    discount_value_pct,
    start_date::date as start_date,
    end_date::date as end_date,
    active
  from source
  where promotion_id is not null
)

select * from renamed
