-- Cloudera 'loudacre' database tables (accounts and basestations)
-- Created to simulate the Hive, Impala, Avro, Parquet & Sqoop lab on macOS

DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS basestations;

-- 1. Table: accounts (matches Cloudera Loudacre schema including city, state, first_name, last_name)
CREATE TABLE accounts (
    acct_num INT PRIMARY KEY,
    acct_create_dt VARCHAR(30),
    acct_close_dt VARCHAR(30),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(10),
    zipcode VARCHAR(15),
    phone_number VARCHAR(20),
    created VARCHAR(30),
    modified VARCHAR(30)
);

INSERT INTO accounts VALUES
(1001, '2023-01-15 09:30:00', NULL, 'Britney', 'Spears', '742 Evergreen Terrace', 'Los Angeles', 'CA', '90001', '555-0101', '2023-01-15 09:30:00', '2025-01-10 12:00:00'),
(1002, '2023-02-20 14:15:00', NULL, 'Roger', 'Miller', '1200 Congress Ave', 'Austin', 'TX', '73301', '555-0102', '2023-02-20 14:15:00', '2025-02-14 15:20:00'),
(1003, '2023-03-10 11:00:00', NULL, 'Alice', 'Johnson', '350 Fifth Ave', 'New York', 'NY', '10118', '555-0103', '2023-03-10 11:00:00', '2025-03-01 10:05:00'),
(1004, '2023-04-05 16:45:00', NULL, 'Carlos', 'Gomez', '400 Biscayne Blvd', 'Miami', 'FL', '33132', '555-0104', '2023-04-05 16:45:00', '2025-03-19 08:30:00'),
(1005, '2023-05-12 10:20:00', NULL, 'Emma', 'Watson', '100 Sunset Blvd', 'Los Angeles', 'CA', '90012', '555-0105', '2023-05-12 10:20:00', '2025-04-05 17:45:00'),
(1006, '2023-06-18 13:10:00', NULL, 'David', 'Smith', '400 Broad St', 'Seattle', 'WA', '98109', '555-0106', '2023-06-18 13:10:00', '2025-05-20 09:15:00'),
(1007, '2023-07-22 08:50:00', NULL, 'Aaron', 'Carter', '850 Wilshire Blvd', 'Los Angeles', 'CA', '90017', '555-0107', '2023-07-22 08:50:00', '2025-06-01 11:10:00'),
(1008, '2023-08-30 15:00:00', NULL, 'tara', 'Davis', '500 Barton Springs Rd', 'Austin', 'TX', '78704', '555-0108', '2023-08-30 15:00:00', '2025-06-15 14:00:00'),
(1009, '2023-09-14 12:25:00', NULL, 'Brian', 'Adams', '200 Broadway', 'New York', 'NY', '10038', '555-0109', '2023-09-14 12:25:00', '2025-07-01 16:30:00');

-- Fix capitalization for consistent alphabetical demonstration
UPDATE accounts SET first_name = 'Tara' WHERE acct_num = 1008;

-- 2. Table: basestations (matches Cloudera Loudacre schema)
CREATE TABLE basestations (
    bs_id INT PRIMARY KEY,
    address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(10),
    zipcode VARCHAR(15),
    latitude REAL,
    longitude REAL
);

INSERT INTO basestations VALUES
(1, '101 Harbor Way', 'Los Angeles', 'CA', '90001', 34.0522, -118.2437),
(2, '250 Tech Ridge Pkwy', 'Austin', 'TX', '73301', 30.2672, -97.7431),
(3, '88 Madison Ave', 'New York', 'NY', '10118', 40.7128, -74.0060),
(4, '15 Ocean Drive', 'Miami', 'FL', '33132', 25.7617, -80.1918),
(5, '700 Pine St', 'Seattle', 'WA', '98109', 47.6062, -122.3321);

