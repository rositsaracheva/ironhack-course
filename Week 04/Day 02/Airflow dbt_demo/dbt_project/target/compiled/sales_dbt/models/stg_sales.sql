SELECT 
    order_id, 
    LOWER(customer) AS customer, 
    LOWER(city) AS city, 
    LOWER(product) AS product, 
    quantity, 
    price, 
    quantity * price AS total_amount 
FROM "warehouse"."main"."sales_raw"