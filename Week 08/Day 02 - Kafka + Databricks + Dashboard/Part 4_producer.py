# Week 08 — Day 02: Kafka + Snowflake + Power BI Integration Project
# Part 4: Real-Time E-Commerce Order Producer (producer.py)
# Student: Rositsa Kaloyanova
# Purpose: Continuously generate fake live e-commerce orders and stream them as JSON messages
#          into the Kafka topic 'ecommerce_orders' every 2 seconds.

# I import KafkaProducer from kafka-python to connect to my local Kafka broker and publish messages.
from kafka import KafkaProducer
# I import Faker so I can generate realistic random customer names for my simulated orders.
from faker import Faker
# I import json so I can convert each Python dictionary (order) into a JSON string before sending.
import json
# I import random so I can pick random products, cities, payment methods, and order amounts.
import random
# I import time so I can pause for 2 seconds between each simulated order.
import time
# I import datetime so I can stamp every order with the exact current timestamp.
from datetime import datetime

# I initialize a Faker generator to create fake customer names.
fake = Faker()

# I create a KafkaProducer client pointing to my local Docker Kafka broker (127.0.0.1:9092 = localhost:9092).
# value_serializer automatically converts every Python dict 'v' into a JSON string and encodes it to UTF-8 bytes
# because Kafka only stores raw bytes.
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# These lists hold the sample product categories, cities, and payment methods for our e-commerce store.
products = ['Laptop', 'Phone', 'Tablet', 'Headphones']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Pune']
payments = ['UPI', 'Card', 'Cash']

# I start order_id at 1 and increment it by 1 for every new order sent.
order_id = 1

print("Starting e-commerce order producer... Press Ctrl-C to stop.")

# I wrap the infinite loop in try/except/finally so pressing Ctrl-C stops cleanly and flushes any queued orders.
try:
    while True:
        # I build one simulated order event as a Python dictionary matching our Snowflake table columns.
        order = {
            "order_id": order_id,
            "customer_name": fake.name(),
            "city": random.choice(cities),
            "product": random.choice(products),
            "amount": round(random.uniform(500, 80000), 2),
            "payment_mode": random.choice(payments),
            "order_time": str(datetime.now())
        }

        # I send the order dictionary to the 'ecommerce_orders' topic (value_serializer turns it into UTF-8 JSON bytes).
        producer.send('ecommerce_orders', value=order)
        # I print the sent order in the terminal so I can watch the live stream happening.
        print("Sent:", order)

        # Move to the next order ID and wait 2 seconds before generating the next order.
        order_id += 1
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopping producer...")
finally:
    # flush() makes sure all queued messages in memory are actually delivered to Kafka before closing.
    producer.flush()
    producer.close()
    print("Producer closed cleanly.")
