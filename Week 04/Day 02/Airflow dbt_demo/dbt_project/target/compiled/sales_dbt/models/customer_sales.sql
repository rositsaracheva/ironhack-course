SELECT 
    customer, 
    COUNT(order_id) AS total_orders, 
    SUM(total_amount) AS revenue, 
    AVG(total_amount) AS average_order 
FROM "warehouse"."main"."stg_sales" 
GROUP BY customer