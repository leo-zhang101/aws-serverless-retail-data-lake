{{
  config(
    materialized='view',
    tags=['staging', 'stores']
  )
}}

with source as (
  select * from {{ source('gold', 'stores') }}
),

renamed as (
  select
    store_id,
    store_name,
    state,
    city,
    opened_at::date as opened_at,
    coalesce(state, 'UNKNOWN') as state_normalised
  from source
  where store_id is not null
)

select * from renamed
