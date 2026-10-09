-- Drop tables if they already exist (clean setup)
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Create customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(50),
    signup_date DATE
);

-- Create products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(8,2)
);

-- Create orders table (contains 22 rows)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    order_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create payments table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT,
    paid_amount DECIMAL(10,2),
    payment_date DATETIME,
    payment_method VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Insert customers (10 rows)
INSERT INTO customers (customer_id, customer_name, email, city, signup_date) VALUES
(1, 'Asha Mehta', 'asha@example.com', 'Pune', '2021-02-15'),
(2, 'Rahul Sharma', 'rahul@example.com', 'Mumbai', '2020-11-20'),
(3, 'Simran Kaur', 'simran@example.com', 'Delhi', '2022-01-05'),
(4, 'Vikram Singh', 'vikram@example.com', 'Bengaluru', '2019-06-10'),
(5, 'Nisha Patel', 'nisha@example.com', 'Ahmedabad', '2021-09-30'),
(6, 'Karan Verma', 'karan@example.com', 'Chennai', '2020-03-22'),
(7, 'Priya Rao', 'priya@example.com', 'Hyderabad', '2022-05-11'),
(8, 'Manish Gupta', 'manish@example.com', 'Pune', '2021-12-01'),
(9, 'Leena Joshi', 'leena@example.com', NULL, '2020-07-07'),
(10, 'Suresh Nair', 'suresh@example.com', 'Kochi', '2018-10-18');

-- Insert products (6 rows)
INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(101, 'Wireless Mouse', 'Accessories', 599.00),
(102, 'Mechanical Keyboard', 'Accessories', 2499.00),
(103, '27-inch Monitor', 'Display', 12999.00),
(104, 'USB-C Adapter', 'Accessories', 499.00),
(105, 'Laptop 14-inch', 'Computers', 54999.00),
(106, 'External SSD 1TB', 'Storage', 7999.00);

-- Insert orders (22 rows)
INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, order_date, status) VALUES
(1001, 1, 101, 1, 599.00, '2022-01-10', 'delivered'),
(1002, 2, 102, 1, 2499.00, '2022-02-15', 'delivered'),
(1003, 3, 104, 2, 499.00, '2022-03-05', 'delivered'),
(1004, 1, 103, 1, 12999.00, '2022-03-20', 'cancelled'),
(1005, 4, 105, 1, 54999.00, '2022-04-02', 'delivered'),
(1006, 5, 101, 2, 599.00, '2022-04-18', 'pending'),
(1007, 6, 106, 1, 7999.00, '2022-05-06', 'delivered'),
(1008, 7, 102, 1, 2499.00, '2022-05-25', 'delivered'),
(1009, 8, 104, 3, 499.00, '2022-06-10', 'delivered'),
(1010, 9, 101, 1, 599.00, '2022-06-21', 'returned'),
(1011, 10, 105, 1, 54999.00, '2022-07-02', 'delivered'),
(1012, 2, 106, 2, 7999.00, '2022-07-18', 'delivered'),
(1013, 3, 101, 4, 599.00, '2022-08-05', 'delivered'),
(1014, 4, 104, 1, 499.00, '2022-08-20', 'delivered'),
(1015, 5, 102, 1, 2499.00, '2022-09-01', 'pending'),
(1016, 6, 103, 1, 12999.00, '2022-09-15', 'delivered'),
(1017, 7, 105, 1, 54999.00, '2022-10-03', 'delivered'),
(1018, 8, 106, 1, 7999.00, '2022-10-25', 'pending'),
(1019, 9, 101, 2, 599.00, '2022-11-11', 'delivered'),
(1020, 10, 104, 5, 499.00, '2022-11-29', 'delivered'),
(1021, 1, 102, 1, 2499.00, '2022-12-05', 'delivered'),
(1022, 2, 101, 3, 599.00, '2022-12-20', 'delivered');

-- Insert payments (8 rows)
INSERT INTO payments (payment_id, order_id, paid_amount, payment_date, payment_method) VALUES
(5001, 1001, 599.00, '2022-01-11 10:10:00', 'card'),
(5002, 1002, 2499.00, '2022-02-16 11:15:00', 'card'),
(5003, 1005, 54999.00, '2022-04-03 09:05:00', 'bank_transfer'),
(5004, 1007, 7999.00, '2022-05-07 14:00:00', 'card'),
(5005, 1011, 54999.00, '2022-07-03 12:20:00', 'bank_transfer'),
(5006, 1012, 15998.00, '2022-07-19 16:45:00', 'card'),
(5007, 1016, 12999.00, '2022-09-16 10:00:00', 'card'),
(5008, 1017, 54999.00, '2022-10-04 18:30:00', 'bank_transfer');

-- Quick verification queries (visible output)
SELECT COUNT(*) AS total_customers FROM customers;
SELECT COUNT(*) AS total_products FROM products;
SELECT COUNT(*) AS total_orders FROM orders;