select
    customer_id,
    customer_name,
    split_part(customer_name, ' ', 1) as first_name,
    split_part(customer_name, ' ', 2) as last_name,
    email,
    city,
    signup_date::date as signup_date
from {{ source('raw', 'customers') }}
