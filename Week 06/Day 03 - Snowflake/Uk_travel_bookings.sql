CREATE DATABASE IF NOT EXISTS travel_db;
CREATE SCHEMA IF NOT EXISTS travel_db.bookings;

CREATE WAREHOUSE IF NOT EXISTS travel_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE WAREHOUSE travel_wh;
USE SCHEMA travel_db.bookings;

CREATE OR REPLACE FILE FORMAT csv_ff
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('');

CREATE OR REPLACE TABLE bookings (
  booking_id INT, booking_date DATE, customer_id STRING, customer_name STRING,
  home_city STRING, destination_city STRING, destination_country STRING,
  package_type STRING, travel_start_date DATE, nights INT, travellers INT,
  price_per_person_gbp NUMBER(10,2), discount_pct NUMBER(5,2),
  payment_mode STRING, status STRING, rating INT
);

-- CREATE OR REPLACE STAGE bookings_stage FILE_FORMAT = csv_ff;

COPY INTO bookings FROM @bookings_stage/uk_travel_bookings.csv ON_ERROR = 'CONTINUE';

-- Q1. Show the first 10 bookings.
SELECT * FROM bookings LIMIT 10;

-- Q2. How many bookings are there in total?
SELECT COUNT(*) AS total_bookings FROM bookings;
-- Q3. List all bookings to Spain.
SELECT booking_id, customer_name, destination_city, travel_start_date
FROM bookings
WHERE destination_country = 'Spain';
-- Q4. Find all Cancelled bookings.
SELECT booking_id, customer_name, destination_city, status
FROM bookings
WHERE status = 'Cancelled';
-- Q5. Which bookings have no discount recorded (NULL)?
SELECT booking_id, customer_name, discount_pct
FROM bookings
WHERE discount_pct IS NULL;
-- Q6. Calculate the revenue for every booking.
SELECT booking_id,
       travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100) AS revenue_gbp
FROM bookings;
-- Q7. Total revenue by package type for non-cancelled bookings, highest first.
SELECT package_type,
       ROUND(SUM(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100)), 2) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY package_type
ORDER BY revenue_gbp DESC;
-- Q8. Which destination country is booked most often?
SELECT destination_country, COUNT(*) AS bookings
FROM bookings
GROUP BY destination_country
ORDER BY bookings DESC
LIMIT 1;
-- Q9. Share of bookings by payment mode.
SELECT payment_mode,
       COUNT(*) AS bookings,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_share
FROM bookings
GROUP BY payment_mode
ORDER BY bookings DESC;
-- LEVEL 2: Q10. Customers with more than 2 bookings.
SELECT customer_name, COUNT(*) AS bookings
FROM bookings
GROUP BY customer_name
HAVING COUNT(*) > 2;
-- Q11. Average rating per destination country (ignore NULL ratings), with at least 2 rated trips.
SELECT destination_country,
       ROUND(AVG(rating), 2) AS avg_rating,
       COUNT(rating) AS rated_trips
FROM bookings
GROUP BY destination_country
HAVING COUNT(rating) >= 2
ORDER BY avg_rating DESC;
-- LEVEL3 - Q12. Work out each trip's return date and how far in advance it was booked.
SELECT booking_id, customer_name,
       DATEADD('day', nights, travel_start_date) AS return_date,
       DATEDIFF('day', booking_date, travel_start_date) AS lead_time_days
FROM bookings;
-- Q13. Monthly bookings count and revenue by travel month.
SELECT DATE_TRUNC('month', travel_start_date) AS travel_month,
       COUNT(*) AS bookings,
       ROUND(SUM(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100)), 2) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY travel_month
ORDER BY travel_month;
-- Q14. Rank customers by total spend within each home city.
SELECT home_city, customer_name, total_spend,
       RANK() OVER (PARTITION BY home_city ORDER BY total_spend DESC) AS city_rank
FROM (
  SELECT home_city, customer_name,
         SUM(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100)) AS total_spend
  FROM bookings
  WHERE status <> 'Cancelled'
  GROUP BY home_city, customer_name
);
-- Q15. For repeat customers, show the gap in days between consecutive bookings.
SELECT customer_name, booking_date,
       DATEDIFF('day',
         LAG(booking_date) OVER (PARTITION BY customer_id ORDER BY booking_date),
         booking_date) AS days_since_last_booking
FROM bookings
QUALIFY COUNT(*) OVER (PARTITION BY customer_id) > 1
ORDER BY customer_name, booking_date;
-- Q16. Top 2 destinations by revenue within each package type (use QUALIFY).
SELECT package_type, destination_city,
       SUM(travellers * price_per_person_gbp) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY package_type, destination_city
QUALIFY ROW_NUMBER() OVER (PARTITION BY package_type ORDER BY SUM(travellers * price_per_person_gbp) DESC) <= 2;
-- Q17. Cancellation rate by package type.
SELECT package_type,
       COUNT(*) AS bookings,
       SUM(IFF(status = 'Cancelled', 1, 0)) AS cancelled,
       ROUND(100 * SUM(IFF(status = 'Cancelled', 1, 0)) / COUNT(*), 1) AS cancel_rate_pct
FROM bookings
GROUP BY package_type;
-- Q18. Segment bookings into Budget, Mid-range and Premium using CASE.
SELECT booking_id, destination_city, price_per_person_gbp,
       CASE
         WHEN price_per_person_gbp < 400 THEN 'Budget'
         WHEN price_per_person_gbp < 900 THEN 'Mid-range'
         ELSE 'Premium'
       END AS price_band
FROM bookings;