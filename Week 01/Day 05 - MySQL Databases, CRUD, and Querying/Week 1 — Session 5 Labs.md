## Quick database creation

`SELECT COUNT(*) AS total_customers FROM customers;`
```
total_customers|
---------------+
             10|
```
`SELECT COUNT(*) AS total_products FROM products;`
```
total_products|
--------------+
             6|
```

`SELECT COUNT(*) AS total_orders FROM orders;`
```
total_orders|
------------+
          22|
```


## Lab 1: Select all orders

`SELECT * FROM orders;`
```
order_id|customer_id|product_id|quantity|unit_price|order_date|status   |
--------+-----------+----------+--------+----------+----------+---------+
    1001|          1|       101|       1|       599|2022-01-10|delivered|
    1002|          2|       102|       1|      2499|2022-02-15|delivered|
    1003|          3|       104|       2|       499|2022-03-05|delivered|
    1004|          1|       103|       1|     12999|2022-03-20|cancelled|
    1005|          4|       105|       1|     54999|2022-04-02|delivered|
    1006|          5|       101|       2|       599|2022-04-18|pending  |
    1007|          6|       106|       1|      7999|2022-05-06|delivered|
    1008|          7|       102|       1|      2499|2022-05-25|delivered|
    1009|          8|       104|       3|       499|2022-06-10|delivered|
    1010|          9|       101|       1|       599|2022-06-21|returned |
    1011|         10|       105|       1|     54999|2022-07-02|delivered|
    1012|          2|       106|       2|      7999|2022-07-18|delivered|
    1013|          3|       101|       4|       599|2022-08-05|delivered|
    1014|          4|       104|       1|       499|2022-08-20|delivered|
    1015|          5|       102|       1|      2499|2022-09-01|pending  |
    1016|          6|       103|       1|     12999|2022-09-15|delivered|
    1017|          7|       105|       1|     54999|2022-10-03|delivered|
    1018|          8|       106|       1|      7999|2022-10-25|pending  |
    1019|          9|       101|       2|       599|2022-11-11|delivered|
    1020|         10|       104|       5|       499|2022-11-29|delivered|
    1021|          1|       102|       1|      2499|2022-12-05|delivered|
    1022|          2|       101|       3|       599|2022-12-20|delivered|
```


## Lab 2: Find order_id, customer_id, quantity, and order_date for orders where quantity > 2.
`
SELECT 
order_id, 
customer_id, 
quantity,
order_date
FROM orders o 
WHERE o.quantity >2 ;
`
```
order_id|customer_id|quantity|order_date|
--------+-----------+--------+----------+
    1009|          8|       3|2022-06-10|
    1013|          3|       4|2022-08-05|
    1020|         10|       5|2022-11-29|
    1022|          2|       3|2022-12-20|
```

## Lab 3: Use IN and BETWEEN
## A. List orders placed by customer_id 1, 2, or 3.

´
SELECT order_id, customer_id, order_date
FROM orders
WHERE customer_id IN (1,2,3)
ORDER BY customer_id, order_date ASC; 

´

´´´
order_id|customer_id|order_date|
--------+-----------+----------+
    1001|          1|2022-01-10|
    1004|          1|2022-03-20|
    1021|          1|2022-12-05|
    1002|          2|2022-02-15|
    1012|          2|2022-07-18|
    1022|          2|2022-12-20|
    1003|          3|2022-03-05|
    1013|          3|2022-08-05|
´´´    
## B. List orders placed between '2022-07-01' and '2022-12-31' (inclusive).

´
SELECT 
order_id,
order_date
FROM orders o 

WHERE order_date BETWEEN '2022-07-01'AND '2022-12-31'
ORDER BY order_date ASC; 
´
´´´
order_id|order_date|
--------+----------+
    1011|2022-07-02|
    1012|2022-07-18|
    1013|2022-08-05|
    1014|2022-08-20|
    1015|2022-09-01|
    1016|2022-09-15|
    1017|2022-10-03|
    1018|2022-10-25|
    1019|2022-11-11|
    1020|2022-11-29|
    1021|2022-12-05|
    1022|2022-12-20|
´´´

## Lab 4: DISTINCT values — cities of customers
## Problem Statement: List distinct cities where customers live.

´ SELECT DISTINCT city FROM customers c ; ` 

´´´
city     |
---------+
Pune     |
Mumbai   |
Delhi    |
Bengaluru|
Ahmedabad|
Chennai  |
Hyderabad|
         |
Kochi    |

´´´

## Lab 5: ORDER BY and LIMIT
## Problem Statement: Find the 5 most recent orders (order_date descending). Show order_id, customer_id, order_date.

´
SELECT 
order_id,
customer_id,
order_date
FROM orders o 
ORDER BY o.order_date DESC
LIMIT 5 ; 
,

´´´
order_id|customer_id|order_date|
--------+-----------+----------+
    1022|          2|2022-12-20|
    1021|          1|2022-12-05|
    1020|         10|2022-11-29|
    1019|          9|2022-11-11|
    1018|          8|2022-10-25|
´´´

## Lab 6: Pattern matching with LIKE
## Concepts Covered
## WHERE ... LIKE /Wildcards %, _
## Problem Statement
## Find products whose name contains 'USB' or 'USB-C' using LIKE. Show product_id and product_name.

´
SELECT product_id, product_name
FROM products
WHERE product_name LIKE '%USB%'; 
´ 

´´´
product_id|product_name |
----------+-------------+
       104|USB-C Adapter|
´´´       

## Lab 7: IS NULL and IS NOT NULL
## Problem Statement
## Find customers whose city is NULL. Then count customers with non-null city.


## Customers with NULL city: ´

´
SELECT customer_id, c.customer_name , c.city AS 'City (NULL)'
FROM customers c 
WHERE c.city IS NULL 
´

´´´
customer_id|customer_name|City (NULL)|     
-----------+-------------+-----------+
          9|Leena Joshi  |           |
´´´
´ --> NOTE: IN DBeaver the table shows a blank space instead of NULL, so I added the NULL in the column name just for reference. I saw that if I click on Grid , it shows the NULL.     

# Count with non-null city:

´
SELECT COUNT(*) AS non_null_city_count
FROM customers
WHERE city IS NOT NULL;
´
´´´
non_null_city_count|
-------------------+
                  9|
´´´

## Lab 8: INSERT a new order (Create CRUD)
## Problem Statement:Add a new order for customer_id 3 buying product_id 106 with quantity 1 on '2023-01-05' status 'pending'. Use order_id 1100.

´
INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, order_date, status)
VALUES (1100, 3, 106, 1, 7999.00, '2023-01-05', 'pending');
´
´
SELECT order_id, customer_id, product_id, quantity, unit_price, order_date, status
FROM orders
WHERE order_id = 1100;
´
´´´
order_id|customer_id|product_id|quantity|unit_price|order_date|status |
--------+-----------+----------+--------+----------+----------+-------+
    1100|          3|       106|       1|      7999|2023-01-05|pending|
'''

## Lab 9: UPDATE with safe practices
## Problem Statement: Change the status of order_id 1006 from 'pending' to 'delivered'. Show the row before and after the update.

## BEFORE:

´
SELECT o.order_id , o.status 
FROM orders o 
WHERE o.order_id = 1006
´
´´´
order_id|status |
--------+-------+
    1006|pending|
´´´

## AFTER UPDATE:

´
UPDATE orders
SET status = 'delivered'
WHERE order_id = 1006;
´
´´´
order_id|status   |
--------+---------+
    1006|delivered|
´´´

## Lab 10: DELETE with safe practices
## Problem Statement: Delete order with order_id 1004 (it was cancelled). Verify the deletion by attempting to SELECT it and by counting remaining rows.

## count before & after

´
SELECT COUNT(*) AS count_before_delete 
FROM orders;
SELECT * 
FROM orders 
WHERE order_id = 1004;
´

´´´
count_before_delete|            
-------------------+             
                 23|            
´´´
---
´´´
order_id|customer_id|product_id|quantity|unit_price|order_date|status   |
--------+-----------+----------+--------+----------+----------+---------+
    1004|          1|       103|       1|     12999|2022-03-20|cancelled|
´´´

´
DELETE FROM orders 
WHERE order_id = 1004 ;

´
SELECT * FROM orders WHERE order_id = 1004;
SELECT COUNT(*) AS count_after_delete FROM orders;
'

´´´
order_id|customer_id|product_id|quantity|unit_price|order_date|status|
--------+-----------+----------+--------+----------+----------+------+
´´´
´ ---> Order id 1004 is not showing anymore after deleteng.´

´´´
count_after_delete|
------------------+
                22|
´´´
´---> orders decreased by 1.

## Lab 11: Aggregation functions

## A. Find total number of orders.

`
SELECT COUNT(*) AS "Total amount of orders:"
FROM orders o 
´
´´´
Total amount of orders:|
-----------------------+
                     22|
´´´                     


## B. Find total quantity ordered across all orders.

´
SELECT SUM(o.quantity)AS 'Total Quantity:' 
FROM orders o 
´

´´´
Total Quantity:|
---------------+
             37|
´´´             


## C. Find average unit_price across orders.

´
SELECT ROUND(AVG(unit_price), 2) AS avg_unit_price 
FROM orders;
´
´´´
avg_unit_price|
--------------+
      10253.55|
´´´      

## D. Find minimum and maximum unit_price recorded in orders.

´
SELECT 
PRINTF('%.2f', MIN(o.unit_price)) AS "Minimum Unit Price",
PRINTF('%.2f', MAX(o.unit_price)) AS "Maximum Unit Price"
FROM orders o 
´
´--> I had to use the PRINTF ('%.2f') to change the format of the numeric result here.
'''
Minimum Unit Price|Maximum Unit Price|
------------------+------------------+
499.00            |54999.00          |

'''

## Lab 12: GROUP BY and HAVING
## Problem Statement: Find total spent per customer (sum of quantity * unit_price) and list customers who spent more than 20000. Show customer_id and total_spent.

´
SELECT o.customer_id,
       PRINTF('%.2f', SUM(o.quantity * o.unit_price), 2) AS total_spent
FROM orders o
GROUP BY o.customer_id
HAVING SUM(o.quantity * o.unit_price) > 20000
ORDER BY total_spent DESC;
´

´´´
customer_id|total_spent|
-----------+-----------+
          7|57498.00   |
         10|57494.00   |
          4|55498.00   |
          6|20998.00   |
          2|20294.00   |
'''

## Lab 13: INNER JOIN — orders with customer names
## Problem Statement
## List order_id, customer_name, product_id, quantity, order_date for all delivered orders. Use INNER JOIN.

´
SELECT o.order_id, c.customer_name, o.product_id, o.quantity, o.order_date
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.status = 'delivered'
ORDER BY o.order_date;
´
´´´
order_id|customer_name|product_id|quantity|order_date|
--------+-------------+----------+--------+----------+
    1001|Asha Mehta   |       101|       1|2022-01-10|
    1002|Rahul Sharma |       102|       1|2022-02-15|
    1003|Simran Kaur  |       104|       2|2022-03-05|
    1005|Vikram Singh |       105|       1|2022-04-02|
    1006|Nisha Patel  |       101|       2|2022-04-18|
    1007|Karan Verma  |       106|       1|2022-05-06|
    1008|Priya Rao    |       102|       1|2022-05-25|
    1009|Manish Gupta |       104|       3|2022-06-10|
    1011|Suresh Nair  |       105|       1|2022-07-02|
    1012|Rahul Sharma |       106|       2|2022-07-18|
    1013|Simran Kaur  |       101|       4|2022-08-05|
    1014|Vikram Singh |       104|       1|2022-08-20|
    1016|Karan Verma  |       103|       1|2022-09-15|
    1017|Priya Rao    |       105|       1|2022-10-03|
    1019|Leena Joshi  |       101|       2|2022-11-11|
    1020|Suresh Nair  |       104|       5|2022-11-29|
    1021|Asha Mehta   |       102|       1|2022-12-05|
    1022|Rahul Sharma |       101|       3|2022-12-20|
´´´

´ --> I have checked that only orders with delivered status have been shown. There were only 3 pending orders.

´´´
order_id|customer_id|product_id|quantity|unit_price|order_date|status |
--------+-----------+----------+--------+----------+----------+-------+
    1015|          5|       102|       1|      2499|2022-09-01|pending|
    1018|          8|       106|       1|      7999|2022-10-25|pending|
    1100|          3|       106|       1|      7999|2023-01-05|pending|

´´´


## Lab 14: LEFT JOIN — find orders without payments
## Problem Statement: Find orders that do not have an entry in payments (left join payments and filter where payment_id IS NULL). Show order_id, customer_id, order_date.

´
SELECT o.order_id, o.customer_id, o.order_date
FROM orders o
LEFT JOIN payments p
  ON o.order_id = p.order_id
WHERE p.payment_id IS NULL
ORDER BY o.order_date;
'

'''
order_id|customer_id|order_date|
--------+-----------+----------+
    1003|          3|2022-03-05|
    1006|          5|2022-04-18|
    1008|          7|2022-05-25|
    1009|          8|2022-06-10|
    1010|          9|2022-06-21|
    1013|          3|2022-08-05|
    1014|          4|2022-08-20|
    1015|          5|2022-09-01|
    1018|          8|2022-10-25|
    1019|          9|2022-11-11|
    1020|         10|2022-11-29|
    1021|          1|2022-12-05|
    1022|          2|2022-12-20|
    1100|          3|2023-01-05|
'''

## Lab 15: Multi-table join with aggregation
## Problem Statement: For each product category, calculate total revenue = SUM(quantity * unit_price) and total_units_sold = SUM(quantity). Show category, total_units_sold, total_revenue. Order by total_revenue DESC.

'
SELECT p.category,
       SUM(o.quantity) AS total_units_sold,
       PRINTF('%.2f', SUM(o.quantity * o.unit_price), 2) AS total_revenue
FROM orders o
JOIN products p
  ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
'

'''
category   |total_units_sold|total_revenue|
-----------+----------------+-------------+
Storage    |               5|39995.00     |
Accessories|              28|23272.00     |
Computers  |               3|164997.00    |
Display    |               1|12999.00     |

'''


## Lab 16: Final Integrated Lab — Business report
## Problem Statement:Create a business report showing top 5 customers by total spending (total_spent = SUM(quantity * unit_price)). 


´
SELECT
  c.customer_id,
  c.customer_name,
  c.city,
  PRINTF('%.2f', SUM(o.quantity * o.unit_price), 2) AS total_spent,
  COUNT(o.order_id) AS total_orders,
  MIN(o.order_date) AS first_order_date,
  MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
WHERE o.status IN ('delivered', 'returned')
  AND o.order_date BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spent DESC
LIMIT 5;
´
´´´
customer_id|customer_name|city     |total_spent|total_orders|first_order_date|last_order_date|
-----------+-------------+---------+-----------+------------+----------------+---------------+
          7|Priya Rao    |Hyderabad|57498.00   |           2|2022-05-25      |2022-10-03     |
         10|Suresh Nair  |Kochi    |57494.00   |           2|2022-07-02      |2022-11-29     |
          4|Vikram Singh |Bengaluru|55498.00   |           2|2022-04-02      |2022-08-20     |
          3|Simran Kaur  |Delhi    |3394.00    |           2|2022-03-05      |2022-08-05     |
          1|Asha Mehta   |Pune     |3098.00    |           2|2022-01-10      |2022-12-05     |

'''






