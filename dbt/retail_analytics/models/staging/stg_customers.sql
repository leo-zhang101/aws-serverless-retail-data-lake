{{
  config(
    materialized='view',
    tags=['staging', 'customers']
  )
}}

with source as (
  select * from {{ source('gold', 'customers') }}
),

renamed as (
  select
    customer_id,
    first_name,
    last_name,
    email,
    state,
    created_at::date as created_at,
    coalesce(state, 'UNKNOWN') as state_normalised
  from source
  where customer_id is not null
)

select * from renamed
