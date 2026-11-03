#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_FILE="$SCRIPT_DIR/loudacre_hive.db"
HDFS_ROOT="$SCRIPT_DIR/hdfs_output"

# Reset previous outputs for a clean run
rm -rf "$HDFS_ROOT" "$DB_FILE"
mkdir -p "$HDFS_ROOT"

# Build the local simulated MySQL 'loudacre' database using SQLite
sqlite3 "$DB_FILE" < "$SCRIPT_DIR/create_loudacre_hive.sql"

echo "============================================================"
echo " Q1: Create an external table in the default database on accounts"
echo "============================================================"
echo ">>> Step 1: Ensure 'accounts' data is imported into HDFS (/Loudacre/accounts)"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --target-dir /Loudacre/accounts
EOF

mkdir -p "$HDFS_ROOT/Loudacre/accounts"
touch "$HDFS_ROOT/Loudacre/accounts/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM accounts;" > "$HDFS_ROOT/Loudacre/accounts/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 9 records into /Loudacre/accounts"

echo ""
echo ">>> Step 2: Create the External Table in Hive (default database)"
cat << 'EOF'
hive> USE default;
OK
hive> CREATE EXTERNAL TABLE accounts (
    >     acct_num INT,
    >     acct_create_dt STRING,
    >     acct_close_dt STRING,
    >     first_name STRING,
    >     last_name STRING,
    >     address STRING,
    >     city STRING,
    >     state STRING,
    >     zipcode STRING,
    >     phone_number STRING,
    >     created STRING,
    >     modified STRING
    > )
    > ROW FORMAT DELIMITED
    > FIELDS TERMINATED BY ','
    > LOCATION '/Loudacre/accounts';
OK
Time taken: 0.245 seconds
hive> SELECT acct_num, first_name, last_name, city, state FROM accounts LIMIT 5;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT acct_num, first_name, last_name, city, state FROM accounts LIMIT 5;"

echo ""
echo "============================================================"
echo " Q2: Create an Avro external table on accounts avro"
echo "============================================================"
echo ">>> Step 1: Import 'accounts' from MySQL as Avro using Sqoop (--as-avrodatafile)"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --target-dir /Loudacre/accounts_avro \
  --as-avrodatafile
EOF

mkdir -p "$HDFS_ROOT/Loudacre/accounts_avro"
touch "$HDFS_ROOT/Loudacre/accounts_avro/_SUCCESS"

# Create the Avro schema file (accounts.avsc) that Sqoop generates automatically
cat << 'EOF' > "$HDFS_ROOT/Loudacre/accounts.avsc"
{
  "type" : "record",
  "name" : "accounts",
  "doc" : "Sqoop import of accounts",
  "fields" : [
    {"name" : "acct_num", "type" : ["null", "int"], "default" : null},
    {"name" : "acct_create_dt", "type" : ["null", "string"], "default" : null},
    {"name" : "acct_close_dt", "type" : ["null", "string"], "default" : null},
    {"name" : "first_name", "type" : ["null", "string"], "default" : null},
    {"name" : "last_name", "type" : ["null", "string"], "default" : null},
    {"name" : "address", "type" : ["null", "string"], "default" : null},
    {"name" : "city", "type" : ["null", "string"], "default" : null},
    {"name" : "state", "type" : ["null", "string"], "default" : null},
    {"name" : "zipcode", "type" : ["null", "string"], "default" : null},
    {"name" : "phone_number", "type" : ["null", "string"], "default" : null},
    {"name" : "created", "type" : ["null", "string"], "default" : null},
    {"name" : "modified", "type" : ["null", "string"], "default" : null}
  ]
}
EOF
sqlite3 -json "$DB_FILE" "SELECT * FROM accounts;" > "$HDFS_ROOT/Loudacre/accounts_avro/part-m-00000.avro"
echo "INFO orm.CompilationManager: Writing avro schema file: accounts.avsc"
echo "INFO mapreduce.ImportJobBase: Retrieved 9 records into /Loudacre/accounts_avro"

echo ""
echo ">>> Step 2: Copy accounts.avsc schema file to HDFS & Create External Avro Table in Hive"
cat << 'EOF'
$ hdfs dfs -put accounts.avsc /Loudacre/accounts.avsc

hive> USE default;
hive> CREATE EXTERNAL TABLE accounts_avro
    > STORED AS AVRO
    > LOCATION '/Loudacre/accounts_avro'
    > TBLPROPERTIES ('avro.schema.url'='hdfs:///Loudacre/accounts.avsc');
OK
Time taken: 0.198 seconds
hive> SELECT acct_num, first_name, last_name, city FROM accounts_avro LIMIT 5;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT acct_num, first_name, last_name, city FROM accounts LIMIT 5;"

echo ""
echo "============================================================"
echo " Q3: Create a Parquet Table on accounts.parquet"
echo "============================================================"
echo ">>> Step 1: Import 'accounts' as Parquet (or convert via Hive/Impala)"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --target-dir /Loudacre/accounts_parquet \
  --as-parquetfile
EOF

mkdir -p "$HDFS_ROOT/Loudacre/accounts_parquet"
touch "$HDFS_ROOT/Loudacre/accounts_parquet/_SUCCESS"

# Use Python + PyArrow to write a real binary Parquet file (accounts.parquet)
python3 - "$DB_FILE" "$HDFS_ROOT/Loudacre/accounts_parquet/accounts.parquet" << 'PYEOF'
import sys, sqlite3
import pandas as pd

db_path, parquet_path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM accounts", conn)
df.to_parquet(parquet_path, index=False)
conn.close()
PYEOF
echo "INFO mapreduce.ImportJobBase: Retrieved 9 records into /Loudacre/accounts_parquet"

echo ""
echo ">>> Step 2: Create the Parquet Table in Hive / Impala"
cat << 'EOF'
hive> USE default;
hive> CREATE EXTERNAL TABLE accounts_parquet (
    >     acct_num INT,
    >     acct_create_dt STRING,
    >     acct_close_dt STRING,
    >     first_name STRING,
    >     last_name STRING,
    >     address STRING,
    >     city STRING,
    >     state STRING,
    >     zipcode STRING,
    >     phone_number STRING,
    >     created STRING,
    >     modified STRING
    > )
    > STORED AS PARQUET
    > LOCATION '/Loudacre/accounts_parquet';
OK
Time taken: 0.212 seconds
hive> SELECT acct_num, first_name, last_name, city, phone_number FROM accounts_parquet LIMIT 5;
EOF
python3 - "$HDFS_ROOT/Loudacre/accounts_parquet/accounts.parquet" << 'PYEOF'
import sys
import pandas as pd
df = pd.read_parquet(sys.argv[1])
print(df[["acct_num", "first_name", "last_name", "city", "phone_number"]].head(5).to_string(index=False))
PYEOF

echo ""
echo "============================================================"
echo " Q4: Import directly through Sqoop table called 'basestations' into Hive"
echo "============================================================"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table basestations \
  --hive-import
EOF

mkdir -p "$HDFS_ROOT/user/hive/warehouse/basestations"
touch "$HDFS_ROOT/user/hive/warehouse/basestations/_SUCCESS"
sqlite3 -separator $'\x01' "$DB_FILE" "SELECT * FROM basestations;" > "$HDFS_ROOT/user/hive/warehouse/basestations/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 5 records."
echo "INFO hive.HiveImport: Loading uploaded data into Hive"
echo "INFO hive.HiveImport: Hive import complete."

echo ""
echo "hive> SHOW TABLES LIKE 'basestations';"
echo "basestations"
echo "hive> SELECT * FROM basestations;"
sqlite3 -header -column "$DB_FILE" "SELECT * FROM basestations;"

echo ""
echo "============================================================"
echo " Q5: Import only first_name and last_name using Sqoop in HDFS"
echo "     for table accounts. Reflect the table on Hive/Impala."
echo "============================================================"
echo ">>> Step 1: Import only first_name and last_name into HDFS with Sqoop"
cat << 'EOF'
$ sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --columns "first_name,last_name" \
  --target-dir /Loudacre/accounts_names
EOF

mkdir -p "$HDFS_ROOT/Loudacre/accounts_names"
touch "$HDFS_ROOT/Loudacre/accounts_names/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT first_name, last_name FROM accounts;" > "$HDFS_ROOT/Loudacre/accounts_names/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 9 records into /Loudacre/accounts_names"

echo ""
echo ">>> Step 2: Check HDFS file content"
echo "$ hdfs dfs -cat /Loudacre/accounts_names/part-m-00000"
cat "$HDFS_ROOT/Loudacre/accounts_names/part-m-00000"

echo ""
echo ">>> Step 3: Create the table in Hive & Refresh Metastore in Impala"
cat << 'EOF'
hive> CREATE EXTERNAL TABLE accounts_names (
    >     first_name STRING,
    >     last_name STRING
    > )
    > ROW FORMAT DELIMITED
    > FIELDS TERMINATED BY ','
    > LOCATION '/Loudacre/accounts_names';
OK

[localhost:21000] default> INVALIDATE METADATA accounts_names;
Query: invalidate metadata accounts_names
Fetched 0 row(s) in 0.15s

[localhost:21000] default> SELECT * FROM accounts_names;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT first_name, last_name FROM accounts;"

echo ""
echo "============================================================"
echo " Q6: Run a query on Hive and Impala both: group the accounts"
echo "     on the basis of city and order them by their names in"
echo "     alphabetical order."
echo "============================================================"
echo ">>> 1) Query in Hive (Grouping by city and ordering alphabetically by name):"
cat << 'EOF'
hive> SELECT city, first_name, last_name
    > FROM accounts
    > GROUP BY city, first_name, last_name
    > ORDER BY city ASC, first_name ASC, last_name ASC;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT city, first_name, last_name FROM accounts GROUP BY city, first_name, last_name ORDER BY city ASC, first_name ASC, last_name ASC;"

echo ""
echo ">>> 2) Same Query + Aggregated City Summary in Impala:"
cat << 'EOF'
[localhost:21000] default> INVALIDATE METADATA accounts;
[localhost:21000] default> SELECT city, first_name, last_name
                         > FROM accounts
                         > GROUP BY city, first_name, last_name
                         > ORDER BY city ASC, first_name ASC, last_name ASC;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT city, first_name, last_name FROM accounts GROUP BY city, first_name, last_name ORDER BY city ASC, first_name ASC, last_name ASC;"

echo ""
cat << 'EOF'
[localhost:21000] default> SELECT city, COUNT(*) AS total_accounts,
                         >        GROUP_CONCAT(first_name || ' ' || last_name, ', ') AS ordered_names
                         > FROM (SELECT city, first_name, last_name FROM accounts ORDER BY city, first_name, last_name) t
                         > GROUP BY city
                         > ORDER BY city ASC;
EOF
sqlite3 -header -column "$DB_FILE" "SELECT city, COUNT(*) AS total_accounts, GROUP_CONCAT(first_name || ' ' || last_name, ', ') AS ordered_names FROM (SELECT city, first_name, last_name FROM accounts ORDER BY city ASC, first_name ASC, last_name ASC) GROUP BY city ORDER BY city ASC;"
echo "============================================================"
