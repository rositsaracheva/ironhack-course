# Lab 2 — Part 5, Exercise 4: End Marker (__EOF__) — Producer
# Student: Rositsa Kaloyanova
# Purpose: Send every line of a text file to Kafka, then send a special final '__EOF__' message
#          so the consumer knows the file is finished and can stop immediately.

import argparse
import os

from confluent_kafka import Producer

# I define the end-of-file marker as a constant so it is easy to read and reuse.
EOF_MARKER = '__EOF__'


def main():
    # I set up command-line arguments for the input file, topic, and Kafka broker address.
    parser = argparse.ArgumentParser(description='Send a text file to Kafka followed by an __EOF__ marker')
    parser.add_argument('file', help='path of the text file to send')
    parser.add_argument('--topic', default='ext4-eof')
    parser.add_argument('--bootstrap', default='localhost:9092')
    args = parser.parse_args()

    # I connect to the Kafka broker and use the file name as the key so all lines and __EOF__ stay in order.
    producer = Producer({'bootstrap.servers': args.bootstrap})
    key = os.path.basename(args.file)
    failed = 0

    def on_delivery(err, msg):
        nonlocal failed
        if err is not None:
            failed += 1
            print(f'Delivery failed: {err}')

    count = 0
    # I open the file and send each line as a Kafka message, just like in Part 2.
    with open(args.file, 'r', encoding='utf-8') as f:
        for line in f:
            value = line.rstrip('\r\n')
            while True:
                try:
                    producer.produce(args.topic, key=key, value=value, callback=on_delivery)
                    break
                except BufferError:
                    producer.poll(1)
            count += 1
            producer.poll(0)

    # After all real lines are queued, I send one final '__EOF__' message with the same key
    # so it arrives right after the last line in the exact same partition.
    while True:
        try:
            producer.produce(args.topic, key=key, value=EOF_MARKER, callback=on_delivery)
            break
        except BufferError:
            producer.poll(1)
    producer.poll(0)

    # Wait until every line AND the '__EOF__' marker are delivered to Kafka.
    producer.flush()
    print(f'Sent {count - failed} of {count} lines + {EOF_MARKER} marker from {args.file} to topic {args.topic}')


if __name__ == '__main__':
    main()
