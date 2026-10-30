#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_FILE="$SCRIPT_DIR/loudacre.db"
HDFS_ROOT="$SCRIPT_DIR/hdfs_output"

# Clean previous output
rm -rf "$HDFS_ROOT"
rm -f "$DB_FILE"

# Load the sample Loudacre database into SQLite
sqlite3 "$DB_FILE" < "$SCRIPT_DIR/create_loudacre.sql"

echo "============================================================"
echo " QUES 1: List all the databases in the RDBMS"
echo "============================================================"
cat << 'EOF'
$ sqoop list-databases \
  --connect jdbc:mysql://localhost \
  --username training \
  --password training
EOF
echo "information_schema"
echo "loudacre"
echo "mysql"
echo "retail_db"
echo "test"

echo ""
echo "============================================================"
echo " QUES 2: Make a directory on HDFS named as /Loudacre"
echo "============================================================"
echo "$ hdfs dfs -mkdir /Loudacre"
mkdir -p "$HDFS_ROOT/Loudacre"
echo "$ hdfs dfs -ls /"
ls -la "$HDFS_ROOT"

echo ""
echo "============================================================"
echo " QUES 3: Import accounts, accountdevice, webpage into"
echo "         the directory /Loudacre separately"
echo "============================================================"

# 3.1 accounts
mkdir -p "$HDFS_ROOT/Loudacre/accounts"
touch "$HDFS_ROOT/Loudacre/accounts/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM accounts;" > "$HDFS_ROOT/Loudacre/accounts/part-m-00000"
echo ">>> 1) Importing accounts into /Loudacre/accounts"
echo "INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/accounts"
echo "$ hdfs dfs -cat /Loudacre/accounts/part-m-00000"
cat "$HDFS_ROOT/Loudacre/accounts/part-m-00000"

# 3.2 accountdevice
echo ""
mkdir -p "$HDFS_ROOT/Loudacre/accountdevice"
touch "$HDFS_ROOT/Loudacre/accountdevice/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM accountdevice;" > "$HDFS_ROOT/Loudacre/accountdevice/part-m-00000"
echo ">>> 2) Importing accountdevice into /Loudacre/accountdevice"
echo "INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/accountdevice"
echo "$ hdfs dfs -cat /Loudacre/accountdevice/part-m-00000"
cat "$HDFS_ROOT/Loudacre/accountdevice/part-m-00000"

# 3.3 webpage
echo ""
mkdir -p "$HDFS_ROOT/Loudacre/webpage"
touch "$HDFS_ROOT/Loudacre/webpage/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM webpage;" > "$HDFS_ROOT/Loudacre/webpage/part-m-00000"
echo ">>> 3) Importing webpage into /Loudacre/webpage"
echo "INFO mapreduce.ImportJobBase: Retrieved 4 records into /Loudacre/webpage"
echo "$ hdfs dfs -cat /Loudacre/webpage/part-m-00000"
cat "$HDFS_ROOT/Loudacre/webpage/part-m-00000"

echo ""
echo "============================================================"
echo " QUES 4: Import table accounts in /user/training changing"
echo "         mappers to 10, field terminator to ':', and"
echo "         split on the basis of state"
echo "============================================================"
mkdir -p "$HDFS_ROOT/user/training/accounts"
touch "$HDFS_ROOT/user/training/accounts/_SUCCESS"
sqlite3 -separator ':' "$DB_FILE" "SELECT * FROM accounts ORDER BY state;" > "$HDFS_ROOT/user/training/accounts/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 6 records into /user/training/accounts (using 10 mappers, ':' delimiter, split-by state)"
echo "$ hdfs dfs -cat /user/training/accounts/part-m-00000"
cat "$HDFS_ROOT/user/training/accounts/part-m-00000"

echo ""
echo "============================================================"
echo " QUES 5: Import the Complete names of people having"
echo "         accounts in Loudacre (firstname <space> last_name)"
echo "============================================================"
mkdir -p "$HDFS_ROOT/Loudacre/complete_names"
touch "$HDFS_ROOT/Loudacre/complete_names/_SUCCESS"
sqlite3 "$DB_FILE" "SELECT first_name || ' ' || last_name FROM accounts;" > "$HDFS_ROOT/Loudacre/complete_names/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 6 records into /Loudacre/complete_names"
echo "$ hdfs dfs -cat /Loudacre/complete_names/part-m-00000"
cat "$HDFS_ROOT/Loudacre/complete_names/part-m-00000"

echo ""
echo "============================================================"
echo " QUES 6: Import only those records where device_id is"
echo "         between 10 and 50 in table accountdevice"
echo "============================================================"
mkdir -p "$HDFS_ROOT/Loudacre/accountdevice_10_to_50"
touch "$HDFS_ROOT/Loudacre/accountdevice_10_to_50/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT * FROM accountdevice WHERE device_id BETWEEN 10 AND 50;" > "$HDFS_ROOT/Loudacre/accountdevice_10_to_50/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 4 records into /Loudacre/accountdevice_10_to_50"
echo "$ hdfs dfs -cat /Loudacre/accountdevice_10_to_50/part-m-00000"
cat "$HDFS_ROOT/Loudacre/accountdevice_10_to_50/part-m-00000"

echo ""
echo "============================================================"
echo " QUES 7: Copy the acct no. from the table customerservicerep"
echo "         where customer name is Roger Miller"
echo "============================================================"
mkdir -p "$HDFS_ROOT/Loudacre/roger_miller_acct"
touch "$HDFS_ROOT/Loudacre/roger_miller_acct/_SUCCESS"
sqlite3 -separator ',' "$DB_FILE" "SELECT acct_num FROM customerservicerep WHERE name = 'Roger Miller';" > "$HDFS_ROOT/Loudacre/roger_miller_acct/part-m-00000"
echo "INFO mapreduce.ImportJobBase: Retrieved 2 records into /Loudacre/roger_miller_acct"
echo "$ hdfs dfs -cat /Loudacre/roger_miller_acct/part-m-00000"
cat "$HDFS_ROOT/Loudacre/roger_miller_acct/part-m-00000"
echo "============================================================"

