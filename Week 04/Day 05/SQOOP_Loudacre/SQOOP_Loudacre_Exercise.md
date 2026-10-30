# LAB | Sqoop Loudacre Exercise

**Week 4 — Day 5: Data Ingestion with Apache Sqoop**

---

## Problem Scenario: Loudacre Inc.
- **Loudacre Inc.** is a leading electronics retailer with more than 1,000 physical stores and an e-commerce website.
- They hired us to bring their relational data (from **MySQL**) into **HDFS (Hadoop)** using **Sqoop** so we can process and analyze it to increase revenue and reduce costs.

### Note About My Setup (Mac OS) & How I Adapted This Exercise
In the official Cloudera training VM, the **`loudacre`** database and all those tables (`accounts`, `accountdevice`, `webpage`, `customerservicerep`) already come pre-installed with data.

Because I am using a **Mac** and I cannot run the Cloudera VM on my computer, I asked **ChatGPT** to help me adapt the exercise so I could see the results here on my Mac:
1. First, I wrote the exact **MySQL / Sqoop / HDFS** commands from class for all 7 questions.
2. Then, with ChatGPT's help, I created a local SQL file ([create_loudacre.sql](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2004/Day%2005/SQOOP_Loudacre/create_loudacre.sql)) with the 4 Loudacre tables and sample data (including *Britney Spears* and *Roger Miller*) and a bash script ([run_loudacre_sqoop.sh](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2004/Day%2005/SQOOP_Loudacre/run_loudacre_sqoop.sh)) using `sqlite3` to simulate the Sqoop imports and generate the `/Loudacre` HDFS folders and `part-m-00000` files locally on my computer.

> **My Quick Notes (To Remember for Class):**
> - **RDBMS (Relational Database Management System):** Software that stores data in tables with rows and columns (in our case, **MySQL**).
> - **Sqoop (SQL + Hadoop):** The tool we use as a bridge to import tables from an RDBMS (MySQL) into Hadoop (HDFS), or export them back.
> - **JDBC (`jdbc:mysql://localhost/loudacre`):** *Java Database Connectivity* — the connector/translator that allows Sqoop (written in Java) to talk to MySQL on `localhost` and open the `loudacre` database.
> - **Default Cloudera Credentials:** Username = `training`, Password = `training`.

---

## Part 1 — Sqoop & HDFS Commands for the 7 Questions

### Ques 1: List all the databases in the RDBMS

```bash
sqoop list-databases \
  --connect jdbc:mysql://localhost \
  --username training \
  --password training
```

> **My Notes:**
> - `sqoop list-databases` connects to MySQL and prints all the database names (same as running `SHOW DATABASES;` inside MySQL).
> - Notice that here we only write `jdbc:mysql://localhost` without a database name at the end, because we just want to see the list of all databases first.
> - From the output list, we will see the **`loudacre`** database that we need for the next questions.

---

### Ques 2: Make a directory on HDFS named as `/Loudacre`

```bash
hdfs dfs -mkdir /Loudacre
```

**To check that the folder was created:**
```bash
hdfs dfs -ls /
```

> **My Notes:**
> - This is a normal HDFS command (not Sqoop).
> - `hdfs dfs -mkdir /Loudacre` creates a new folder called `Loudacre` at the root (`/`) of HDFS so we can save our imported tables inside it.

---

### Ques 3: Import `accounts`, `accountdevice`, `webpage` into the directory `/Loudacre` separately

#### 1. Import `accounts` table:
```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --target-dir /Loudacre/accounts
```

#### 2. Import `accountdevice` table:
```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accountdevice \
  --target-dir /Loudacre/accountdevice
```

#### 3. Import `webpage` table:
```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table webpage \
  --target-dir /Loudacre/webpage
```

> **My Notes:**
> - We run `sqoop import` three separate times, once for each table (`accounts`, `accountdevice`, and `webpage`).
> - We use `--target-dir /Loudacre/<table_name>` so each table gets its own subfolder inside `/Loudacre`.
> - **Alternative shortcut:** Instead of `--target-dir`, we could also write `--warehouse-dir /Loudacre`. The difference is that `--warehouse-dir` automatically creates a subfolder with the table's name inside `/Loudacre`.
> - **Troubleshooting tip:** By default, Sqoop uses **4 mappers** and needs a **Primary Key** to split the work. If `accountdevice` or `webpage` does not have a Primary Key in MySQL and gives an error, we just add `-m 1` at the end of the command.

---

### Ques 4: Import table `accounts` in `/user/training` changing the mappers to 10 and changing the field terminator to `':'`. Also split them on the basis of `state`.

```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --target-dir /user/training/accounts \
  --fields-terminated-by ':' \
  --split-by state \
  -m 10
```

> **My Notes (What each part does):**
> - `--target-dir /user/training/accounts`: Saves the imported data inside `/user/training/accounts` in HDFS (note: `/user/training` is also the default home folder in Cloudera).
> - `-m 10` (or `--num-mappers 10`): Changes the number of parallel mappers from the default (4) to **10**. This means Sqoop will create 10 part files (`part-m-00000` to `part-m-00009`).
> - `--fields-terminated-by ':'`: Changes the separator between columns from the default comma (`,`) to a colon (`:`). For example: `1001:Britney:Spears:CA:555-0101`.
> - `--split-by state`: Normally Sqoop splits the data across mappers using the Primary Key (`acct_num`). Here we tell Sqoop to divide the work among the 10 mappers using the `state` column instead.

---

### Ques 5: Import the Complete names of people having accounts in Loudacre
*(Example: `firstname <space> last_name` -> `Britney Spears`)*

```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --query "SELECT CONCAT(first_name, ' ', last_name) FROM accounts WHERE \$CONDITIONS" \
  --target-dir /Loudacre/complete_names \
  -m 1
```

**To check the result in HDFS:**
```bash
hdfs dfs -cat /Loudacre/complete_names/part-m-00000
```

> **My Notes:**
> - Because we want to join two columns (`first_name` and `last_name`) with a space in the middle, we cannot just use `--columns`. Instead, we use `--query` with the SQL function `CONCAT(first_name, ' ', last_name)`.
> - **Important rules when using `--query` in Sqoop:**
>   1. You **cannot** use `--table` when you use `--query`.
>   2. You **must** write `WHERE \$CONDITIONS` at the end of the SQL query (Sqoop uses this internally to split queries).
>   3. You **must** specify `--target-dir` (because Sqoop doesn't have a `--table` name to create the folder automatically).
>   4. You **must** either set `-m 1` (1 mapper) or add `--split-by`. Using `-m 1` is the easiest and safest way!

---

### Ques 6: Import only those records where `device_id` is between 10 and 50 in table `accountdevice`.

```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accountdevice \
  --where "device_id BETWEEN 10 AND 50" \
  --target-dir /Loudacre/accountdevice_10_to_50 \
  -m 1
```

> **My Notes:**
> - `--where "device_id BETWEEN 10 AND 50"`: Filters the rows just like a `WHERE` clause in SQL, so Sqoop only imports rows where `device_id` is from 10 to 50.
> - We could also write `--where "device_id >= 10 AND device_id <= 50"`, both work the exact same way.
> - We use a new `--target-dir` (`/Loudacre/accountdevice_10_to_50`) because HDFS does not allow importing into a folder that already exists!

---

### Ques 7: Copy the `acct no.` from the table `customerservicerep` where customer name is `Roger Miller`.

```bash
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table customerservicerep \
  --columns "acct_num" \
  --where "name = 'Roger Miller'" \
  --target-dir /Loudacre/roger_miller_acct \
  -m 1
```

> **My Notes:**
> - Here we need to filter both **columns** and **rows**:
>   - `--columns "acct_num"`: Imports only the account number column (instead of the whole table).
>   - `--where "name = 'Roger Miller'"`: Imports only the row(s) where the customer name is `'Roger Miller'`. Notice we use double quotes `" "` on the outside and single quotes `' '` around `'Roger Miller'`.
> - Finally, we can check the account number imported into HDFS with:
>   ```bash
>   hdfs dfs -cat /Loudacre/roger_miller_acct/part-m-00000
>   ```

---

## Part 2 — How I Simulated the `loudacre` Database on My Mac

Because I don't have the Cloudera VM with the pre-installed `loudacre` database on my Mac, ChatGPT helped me create [create_loudacre.sql](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2004/Day%2005/SQOOP_Loudacre/create_loudacre.sql) with sample data for the 4 tables (`accounts`, `accountdevice`, `webpage`, and `customerservicerep`) and [run_loudacre_sqoop.sh](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2004/Day%2005/SQOOP_Loudacre/run_loudacre_sqoop.sh) to see the output in my terminal:

### 1. Sample SQL Tables (`create_loudacre.sql`)
```sql
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
```

---

### 2. My Terminal Result (`run_loudacre_sqoop.sh`)

Here is the output from my terminal when running the script for all 7 questions:

```text
(base) rosi@Calculon IronHack Course  % bash "Week 04/Day 05/SQOOP_Loudacre/run_loudacre_sqoop.sh"
============================================================
 QUES 1: List all the databases in the RDBMS
============================================================
$ sqoop list-databases \
  --connect jdbc:mysql://localhost \
  --username training \
  --password training
information_schema
loudacre
mysql
retail_db
test

============================================================
 QUES 2: Make a directory on HDFS named as /Loudacre
============================================================
$ hdfs dfs -mkdir /Loudacre
$ hdfs dfs -ls /
total 0
drwxr-xr-x@ 3 rosi  staff   96 Oct 30 17:31 .
drwxr-xr-x@ 7 rosi  staff  224 Oct 30 17:31 ..
drwxr-xr-x@ 2 rosi  staff   64 Oct 30 17:31 Loudacre

============================================================
 QUES 3: Import accounts, accountdevice, webpage into
         the directory /Loudacre separately
============================================================
>>> 1) Importing accounts into /Loudacre/accounts
INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/accounts
$ hdfs dfs -cat /Loudacre/accounts/part-m-00000
1001,Britney,Spears,CA,555-0101
1002,Roger,Miller,TX,555-0102
1003,Alice,Johnson,NY,555-0103
1004,Carlos,Gomez,FL,555-0104
1005,Emma,Watson,CA,555-0105
1006,David,Smith,WA,555-0106

>>> 2) Importing accountdevice into /Loudacre/accountdevice
INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/accountdevice
$ hdfs dfs -cat /Loudacre/accountdevice/part-m-00000
1,1001,5,2025-01-10
2,1002,12,2025-02-14
3,1003,25,2025-03-01
4,1004,48,2025-03-19
5,1005,50,2025-04-05
6,1006,75,2025-05-20

>>> 3) Importing webpage into /Loudacre/webpage
INFO mapreduce.ImportJobBase: Retrieved 4 records into /Loudacre/webpage
$ hdfs dfs -cat /Loudacre/webpage/part-m-00000
1,/index.html,logo.png,style.css
2,/phones.html,sorrento.jpg,titanic.jpg
3,/support.html,faq.pdf,contact.js
4,/account.html,profile.css,auth.js

============================================================
 QUES 4: Import table accounts in /user/training changing
         mappers to 10, field terminator to ':', and
         split on the basis of state
============================================================
INFO mapreduce.ImportJobBase: Retrieved 6 records into /user/training/accounts (using 10 mappers, ':' delimiter, split-by state)
$ hdfs dfs -cat /user/training/accounts/part-m-00000
1001:Britney:Spears:CA:555-0101
1005:Emma:Watson:CA:555-0105
1004:Carlos:Gomez:FL:555-0104
1003:Alice:Johnson:NY:555-0103
1002:Roger:Miller:TX:555-0102
1006:David:Smith:WA:555-0106

============================================================
 QUES 5: Import the Complete names of people having
         accounts in Loudacre (firstname <space> last_name)
============================================================
INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/complete_names
$ hdfs dfs -cat /Loudacre/complete_names/part-m-00000
Britney Spears
Roger Miller
Alice Johnson
Carlos Gomez
Emma Watson
David Smith

============================================================
 QUES 6: Import only those records where device_id is
         between 10 and 50 in table accountdevice
============================================================
INFO mapreduce.ImportJobBase: Retrieved 4 records into /Loudacre/accountdevice_10_to_50
$ hdfs dfs -cat /Loudacre/accountdevice_10_to_50/part-m-00000
2,1002,12,2025-02-14
3,1003,25,2025-03-01
4,1004,48,2025-03-19
5,1005,50,2025-04-05

============================================================
 QUES 7: Copy the acct no. from the table customerservicerep
         where customer name is Roger Miller
============================================================
INFO mapreduce.ImportJobBase: Retrieved 2 records into /Loudacre/roger_miller_acct
$ hdfs dfs -cat /Loudacre/roger_miller_acct/part-m-00000
1002
1002
============================================================
```
