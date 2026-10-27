SELECT
    CAST(order_id AS INTEGER) AS order_id,
    TRIM(customer) AS customer_name,
    TRIM(product) AS product_name,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(price AS DECIMAL(12, 2)) AS unit_price,
    CAST(quantity AS DECIMAL(12, 2))
        * CAST(price AS DECIMAL(12, 2)) AS sales_amount
FROM {{ ref('sales') }}
WHERE quantity IS NOT NULL
    AND price IS NOT NULL
    AND quantity > 0
    AND price >= 0
