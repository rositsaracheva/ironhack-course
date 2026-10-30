# CLASS Exercise: Import Two Tables from MySQL Using Sqoop

**Week 4 — Day 5**

---

## Question
> **Ques:** Import any two tables from the database in MySQL using Sqoop.  
> **Questions from the terminal:** Where is the end data? What format?

### Note About My Setup (Mac OS)
Because I am using a **Mac** and I cannot run the Cloudera VM on my computer, following the chatGPT instructions, I wrote the exact **MySQL** and **Sqoop** commands from class, and I also created a local SQL setup (`sqlite3`) and a bash script (`sqoop_import.sh`) on my Mac to simulate the database and generate the exact HDFS output files (`_SUCCESS` and `part-m-00000`) in my terminal.

---

## 1. Terminal 1 — Create Two Tables in MySQL

In the first terminal, we log into MySQL with the user and password `training`:

```bash
mysql -utraining -ptraining
```

Then we check the databases and create a database called `retail_db` with two tables (`employees` and `departments`), I asked ChatGPT to give as well the data to insert into the tables so I don´t have to create it manually :

```sql
SHOW DATABASES;

CREATE DATABASE IF NOT EXISTS retail_db;
USE retail_db;

-- Clean up if tables already exist
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- Table 1: employees (with a 'sales' column so we can filter with sales > 34000)
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    sales INT
);

INSERT INTO employees (emp_id, name, department, sales) VALUES
(1, 'Alice', 'Electronics', 45000),
(2, 'Bob', 'Clothing', 28000),
(3, 'Charlie', 'Electronics', 52000),
(4, 'Diana', 'Home', 34000),
(5, 'Evan', 'Clothing', 61000),
(6, 'Fiona', 'Home', 39500);

-- Table 2: departments
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    location VARCHAR(50),
    manager VARCHAR(50)
);

INSERT INTO departments (dept_id, dept_name, location, manager) VALUES
(101, 'Electronics', 'London', 'Sarah Jenkins'),
(102, 'Clothing', 'Manchester', 'David Chen'),
(103, 'Home', 'Birmingham', 'Priya Patel'),
(104, 'Sports', 'Edinburgh', 'Liam O''Connor');

-- Check the tables and data
SHOW TABLES;
SELECT * FROM employees;
SELECT * FROM departments;
```

---

## 2. Terminal 2 — Import the Two Tables with Sqoop

In a second terminal window (outside of MySQL), we run `sqoop import` to bring both tables from MySQL into HDFS.

### Import Table 1 (`employees` — filtering columns and `sales > 34000` like in the class example):
```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table employees \
  --columns "emp_id,name,sales" \
  --where "sales>34000"
```

### Import Table 2 (`departments` — importing the full table):
```bash
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table departments
```

### Check the imported files in HDFS:
```bash
hdfs dfs -ls /user/training/employees
hdfs dfs -cat /user/training/employees/part-m-00000

hdfs dfs -ls /user/training/departments
hdfs dfs -cat /user/training/departments/part-m-00000
```

---

## 3. What I Created to Run It on My Mac (`sqoop_import.sh`)

Since I don't have Cloudera installed on macOS, ChatGPT told me to create this bash script (`sqoop_import.sh`) to build the database locally, run the queries, and create the same HDFS folder structure and `part-m-00000` files:

```bash
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_FILE="$SCRIPT_DIR/retail_db.db"
HDFS_ROOT="$SCRIPT_DIR/hdfs_output"

echo "============================================================"
echo " STEP 1: Terminal 1 — MySQL Database & Tables (retail_db)"
echo " Command in class: mysql -utraining -ptraining"
echo "============================================================"
sqlite3 "$DB_FILE" < "$SCRIPT_DIR/create_tables.sql" >/dev/null

echo ""
echo "mysql> SHOW TABLES;"
sqlite3 -header -column "$DB_FILE" "SELECT name AS Tables_in_retail_db FROM sqlite_master WHERE type='table';"

echo ""
echo "mysql> SELECT * FROM employees;"
sqlite3 -header -column "$DB_FILE" "SELECT * FROM employees;"

echo ""
echo "mysql> SELECT * FROM departments;"
sqlite3 -header -column "$DB_FILE" "SELECT * FROM departments;"

echo ""
echo "============================================================"
echo " STEP 2: Terminal 2 — Sqoop Import (2 Tables)"
echo "============================================================"

echo ""
echo ">>> Importing Table 1: employees (with --columns and --where 'sales>34000')"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table employees \
  --columns "emp_id,name,sales" \
  --where "sales>34000"
EOF

mkdir -p "$HDFS_ROOT/user/training/employees"
touch "$HDFS_ROOT/user/training/employees/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT emp_id, name, sales FROM employees WHERE sales > 34000;" > "$HDFS_ROOT/user/training/employees/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 4 records into /user/training/employees"

echo ""
echo ">>> Importing Table 2: departments (full table import)"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table departments
EOF

mkdir -p "$HDFS_ROOT/user/training/departments"
touch "$HDFS_ROOT/user/training/departments/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM departments;" > "$HDFS_ROOT/user/training/departments/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 4 records into /user/training/departments"

echo ""
echo "============================================================"
echo " STEP 3: Where is the end data & what format is it in?"
echo "============================================================"
echo "• End Data Location (HDFS): /user/training/employees and /user/training/departments"
echo "• End Data Format: Comma-separated plain text (CSV) inside part-m-00000 files"

echo ""
echo "$ hdfs dfs -ls /user/training/employees"
ls -la "$HDFS_ROOT/user/training/employees"

echo ""
echo "$ hdfs dfs -cat /user/training/employees/part-m-00000"
cat "$HDFS_ROOT/user/training/employees/part-m-00000"

echo ""
echo "$ hdfs dfs -ls /user/training/departments"
ls -la "$HDFS_ROOT/user/training/departments"

echo ""
echo "$ hdfs dfs -cat /user/training/departments/part-m-00000"
cat "$HDFS_ROOT/user/training/departments/part-m-00000"
echo "============================================================"
```

---

## 4. My Terminal Result

Here is the exact output from my terminal when running the script:

```text
(base) rosi@Calculon IronHack Course  % bash "Week 04/Day 05/sqoop_import.sh"
============================================================
 STEP 1: Terminal 1 — MySQL Database & Tables (retail_db)
 Command in class: mysql -utraining -ptraining
============================================================

mysql> SHOW TABLES;
Tables_in_retail_db
-------------------
employees
departments

mysql> SELECT * FROM employees;
emp_id   name    department   sales
------  -------  -----------  -----
     1  Alice    Electronics  45000
     2  Bob      Clothing     28000
     3  Charlie  Electronics  52000
     4  Diana    Home         34000
     5  Evan     Clothing     61000
     6  Fiona    Home         39500

mysql> SELECT * FROM departments;
dept_id   dept_name    location      manager
-------  -----------  ----------  -------------
    101  Electronics  London      Sarah Jenkins
    102  Clothing     Manchester  David Chen
    103  Home         Birmingham  Priya Patel
    104  Sports       Edinburgh   Liam O'Connor

============================================================
 STEP 2: Terminal 2 — Sqoop Import (2 Tables)
============================================================

>>> Importing Table 1: employees (with --columns and --where 'sales>34000')
$ sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table employees \
  --columns "emp_id,name,sales" \
  --where "sales>34000"
INFO mapreduce.ImportJobBase: Retrieved 4 records into /user/training/employees

>>> Importing Table 2: departments (full table import)
$ sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username training \
  --password training \
  --table departments
INFO mapreduce.ImportJobBase: Retrieved 4 records into /user/training/departments

============================================================
 STEP 3: Where is the end data & what format is it in?
============================================================
• End Data Location (HDFS): /user/training/employees and /user/training/departments
• End Data Format: Comma-separated plain text (CSV) inside part-m-00000 files

$ hdfs dfs -ls /user/training/employees
total 8
-rw-r--r--@ 1 rosi  staff    0 Oct 30 10:35 _SUCCESS
drwxr-xr-x@ 4 rosi  staff  128 Oct 30 10:30 .
drwxr-xr-x@ 4 rosi  staff  128 Oct 30 10:30 ..
-rw-r--r--@ 1 rosi  staff   57 Oct 30 10:35 part-m-00000

$ hdfs dfs -cat /user/training/employees/part-m-00000
1,Alice,45000
3,Charlie,52000
5,Evan,61000
6,Fiona,39500

$ hdfs dfs -ls /user/training/departments
total 8
-rw-r--r--@ 1 rosi  staff    0 Oct 30 10:35 _SUCCESS
drwxr-xr-x@ 4 rosi  staff  128 Oct 30 10:30 .
drwxr-xr-x@ 4 rosi  staff  128 Oct 30 10:30 ..
-rw-r--r--@ 1 rosi  staff  139 Oct 30 10:35 part-m-00000

$ hdfs dfs -cat /user/training/departments/part-m-00000
101,Electronics,London,Sarah Jenkins
102,Clothing,Manchester,David Chen
103,Home,Birmingham,Priya Patel
104,Sports,Edinburgh,Liam O'Connor
============================================================
```

---

## 5. Answers to the Final Questions

### 1. Where is the end data?
- The end data is saved inside **HDFS (Hadoop Distributed File System)**.
- Because we did not add `--target-dir`, Sqoop automatically saves each table in a new folder with the table's name inside our user's home directory in HDFS:
  - `/user/training/employees`
  - `/user/training/departments`
- Inside each folder, Sqoop creates:
  - `_SUCCESS` (an empty file that shows the import finished without errors).
  - `part-m-00000` (and other `part-m-*` files depending on the number of mappers), which contain the actual rows imported from MySQL.

### 2. What format is the end data in?
- By default, the end data is in **comma-separated plain text format (CSV / text files)**.
- Each row from the MySQL table is saved as one line of text, and each column is separated by a comma (`,`), for example:
  `1,Alice,45000`
