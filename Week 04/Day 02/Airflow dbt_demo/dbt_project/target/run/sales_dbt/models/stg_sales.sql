
    

    create  table
      "warehouse"."main"."stg_sales__dbt_tmp"
  
    
    as (
      SELECT 
    order_id, 
    LOWER(customer) AS customer, 
    LOWER(city) AS city, 
    LOWER(product) AS product, 
    quantity, 
    price, 
    quantity * price AS total_amount 
FROM "warehouse"."main"."sales_raw"
    );
    
  