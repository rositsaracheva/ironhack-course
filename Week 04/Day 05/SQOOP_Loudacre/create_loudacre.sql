-- Sample Loudacre database tables created to simulate Cloudera's pre-installed 'loudacre' database on Mac

DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS accountdevice;
DROP TABLE IF EXISTS webpage;
DROP TABLE IF EXISTS customerservicerep;

-- 1. Table: accounts
CREATE TABLE accounts (
    acct_num INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    state VARCHAR(10),
    phone_number VARCHAR(20)
);

INSERT INTO accounts (acct_num, first_name, last_name, state, phone_number) VALUES
(1001, 'Britney', 'Spears', 'CA', '555-0101'),
(1002, 'Roger', 'Miller', 'TX', '555-0102'),
(1003, 'Alice', 'Johnson', 'NY', '555-0103'),
(1004, 'Carlos', 'Gomez', 'FL', '555-0104'),
(1005, 'Emma', 'Watson', 'CA', '555-0105'),
(1006, 'David', 'Smith', 'WA', '555-0106');

-- 2. Table: accountdevice
CREATE TABLE accountdevice (
    id INT PRIMARY KEY,
    acct_id INT,
    device_id INT,
    activation_date VARCHAR(20)
);

INSERT INTO accountdevice (id, acct_id, device_id, activation_date) VALUES
(1, 1001, 5, '2025-01-10'),
(2, 1002, 12, '2025-02-14'),
(3, 1003, 25, '2025-03-01'),
(4, 1004, 48, '2025-03-19'),
(5, 1005, 50, '2025-04-05'),
(6, 1006, 75, '2025-05-20');

-- 3. Table: webpage
CREATE TABLE webpage (
    page_id INT PRIMARY KEY,
    page_url VARCHAR(100),
    associated_files VARCHAR(100)
);

INSERT INTO webpage (page_id, page_url, associated_files) VALUES
(1, '/index.html', 'logo.png,style.css'),
(2, '/phones.html', 'sorrento.jpg,titanic.jpg'),
(3, '/support.html', 'faq.pdf,contact.js'),
(4, '/account.html', 'profile.css,auth.js');

-- 4. Table: customerservicerep
CREATE TABLE customerservicerep (
    rep_id INT PRIMARY KEY,
    acct_num INT,
    name VARCHAR(100),
    issue_type VARCHAR(50)
);

INSERT INTO customerservicerep (rep_id, acct_num, name, issue_type) VALUES
(101, 1001, 'Britney Spears', 'Billing Question'),
(102, 1002, 'Roger Miller', 'Screen Replacement'),
(103, 1003, 'Alice Johnson', 'Network Coverage'),
(104, 1002, 'Roger Miller', 'Plan Upgrade');

