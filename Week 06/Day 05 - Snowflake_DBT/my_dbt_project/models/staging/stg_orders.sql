with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        product_id,
        order_date::date as order_date,
        quantity,
        unit_price::number(10,2) as unit_price,
        lower(payment_status) as order_status,
        (quantity * unit_price)::number(10,2) as order_amount
    from source
)

select * from renamed
