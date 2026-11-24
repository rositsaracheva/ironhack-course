# Week 08 — Day 02: Kafka + Databricks + Dashboard Integration Project
# Part 7: Kafka Consumer -> Databricks Delta Table (Part 7_consumer_databricks.py)
# Student: Rositsa Kaloyanova
# Purpose: Read live JSON order events from the Kafka topic 'ecommerce_orders' and insert them
#          into my Databricks Unity Catalog table 'workspace.kafka_demo.orders'.

# I import argparse so I can optionally pass an --idle timeout when testing (or 0 to listen forever).
import argparse
# I import json so I can deserialize raw UTF-8 bytes from Kafka back into Python dictionaries.
import json
# I import os to read my Databricks credentials safely from environment variables.
import os
# I import time to track batch timing and idle shutdown.
import time

# I import KafkaConsumer from kafka-python to subscribe to the 'ecommerce_orders' topic.
from kafka import KafkaConsumer
# I import load_dotenv to load my secret Databricks credentials from the local gitignored .env file.
from dotenv import load_dotenv
# I import Databricks' official SQL connector to insert rows into workspace.kafka_demo.orders.
from databricks import sql


def flush_batch(cursor, batch):
    """Insert a batch of order tuples into workspace.kafka_demo.orders in one fast SQL statement."""
    if not batch:
        return 0
    # I build a multi-row parameterized INSERT statement using '?' placeholders.
    # Using placeholders is much safer than f-strings (it won't break if a customer name has an apostrophe like O'Brien)
    # and inserting in batches is much faster than sending 100+ separate HTTP requests to Databricks.
    placeholders = ", ".join(["(?, ?, ?, ?, ?, ?, ?)"] * len(batch))
    query = f"""
        INSERT INTO workspace.kafka_demo.orders
        (order_id, customer_name, city, product, amount, payment_mode, order_time)
        VALUES {placeholders}
    """
    # I flatten the list of 7-element tuples into one flat list of parameters matching all '?' placeholders.
    params = [val for row in batch for val in row]
    cursor.execute(query, params)
    inserted = len(batch)
    batch.clear()
    return inserted


def main():
    # I define optional command-line arguments so I can run either continuously (--idle 0) or auto-stop (--idle 5).
    parser = argparse.ArgumentParser(description='Stream Kafka ecommerce_orders into Databricks')
    parser.add_argument('--topic', default='ecommerce_orders')
    parser.add_argument('--bootstrap', default='127.0.0.1:9092')
    parser.add_argument('--group', default=f'databricks-consumer-{int(time.time())}')
    parser.add_argument('--batch-size', type=int, default=50,
                        help='number of orders to group into one Databricks INSERT statement')
    parser.add_argument('--idle', type=int, default=0,
                        help='stop after this many seconds without messages (0 = run forever until Ctrl-C)')
    args = parser.parse_args()

    # Step 1: Load my Databricks credentials from the .env file in the same folder as this script.
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(env_path)
    host = os.getenv('DATABRICKS_SERVER_HOSTNAME', '').strip()
    http_path = os.getenv('DATABRICKS_HTTP_PATH', '').strip()
    token = os.getenv('DATABRICKS_ACCESS_TOKEN', '').strip()

    if not (host and http_path and token):
        raise SystemExit('Missing Databricks credentials in .env (HOSTNAME, HTTP_PATH, ACCESS_TOKEN).')

    # Step 2: Create the KafkaConsumer subscribed to 'ecommerce_orders'.
    # auto_offset_reset='earliest' ensures a new consumer group reads from the very first message.
    # value_deserializer converts each raw UTF-8 byte message back into a Python dictionary.
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap,
        group_id=args.group,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    )

    # Step 3: Connect to my Databricks SQL Warehouse and open a cursor for running INSERT statements.
    print(f'Connecting to Databricks ({host})...')
    conn = sql.connect(server_hostname=host, http_path=http_path, access_token=token)
    cursor = conn.cursor()
    print(f'Listening to Kafka topic "{args.topic}"... (Press Ctrl-C to stop)')

    batch = []
    total_inserted = 0
    last_message_time = time.time()

    try:
        while True:
            # poll() checks Kafka for up to 1 second (1000 ms) and returns any available messages.
            records = consumer.poll(timeout_ms=1000)

            if records:
                for topic_partition, messages in records.items():
                    for message in messages:
                        data = message.value
                        # I extract all 7 fields in the exact column order of workspace.kafka_demo.orders.
                        batch.append((
                            int(data['order_id']),
                            str(data['customer_name']),
                            str(data['city']),
                            str(data['product']),
                            float(data['amount']),
                            str(data['payment_mode']),
                            str(data['order_time']),
                        ))
                        last_message_time = time.time()

                        # When the batch reaches --batch-size (e.g., 50 orders), I insert them all at once.
                        if len(batch) >= args.batch_size:
                            count = flush_batch(cursor, batch)
                            total_inserted += count
                            print(f'Inserted batch of {count} orders into Databricks (total: {total_inserted})')
            else:
                # If no new messages arrived during this 1-second poll, I flush any remaining partial batch right away
                # so the dashboard sees the latest orders immediately without waiting for a full batch.
                if batch:
                    count = flush_batch(cursor, batch)
                    total_inserted += count
                    print(f'Inserted batch of {count} orders into Databricks (total: {total_inserted})')

                # If --idle > 0 and we have been quiet for longer than --idle seconds, stop cleanly.
                if args.idle > 0 and (time.time() - last_message_time) >= args.idle:
                    print(f'Idle timeout ({args.idle}s) reached — stopping cleanly.')
                    break
    except KeyboardInterrupt:
        print('\nStopping consumer...')
    finally:
        # Flush any leftover orders, then close both the Databricks connection and Kafka consumer cleanly.
        if batch:
            count = flush_batch(cursor, batch)
            total_inserted += count
            print(f'Inserted final batch of {count} orders into Databricks (total: {total_inserted})')
        cursor.close()
        conn.close()
        consumer.close()
        print(f'Done! Total orders inserted into workspace.kafka_demo.orders: {total_inserted}')


if __name__ == '__main__':
    main()
