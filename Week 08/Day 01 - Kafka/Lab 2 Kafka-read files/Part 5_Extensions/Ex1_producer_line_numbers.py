# Lab 2 — Part 5, Exercise 1: Line Numbers — Producer
# Student: Rositsa Kaloyanova
# Purpose: Read a text file line by line, prefix each line with its line number (e.g., "1: ..."),
#          and send each numbered line as a message to a Kafka topic.

import argparse
import os

from confluent_kafka import Producer


def main():
    # I set up command-line arguments for the input file, target topic, and Kafka broker address.
    parser = argparse.ArgumentParser(description='Send a text file to Kafka with line numbers')
    parser.add_argument('file', help='path of the text file to send')
    parser.add_argument('--topic', default='ext1-line-numbers')
    parser.add_argument('--bootstrap', default='localhost:9092')
    args = parser.parse_args()

    # I connect to the local Kafka broker and use the file name as the key so all lines stay in order.
    producer = Producer({'bootstrap.servers': args.bootstrap})
    key = os.path.basename(args.file)
    failed = 0

    # Callback function to report if any message fails to be delivered.
    def on_delivery(err, msg):
        nonlocal failed
        if err is not None:
            failed += 1
            print(f'Delivery failed: {err}')

    count = 0
    # I open the file with UTF-8 encoding and use enumerate(f, start=1) so the first line is number 1 (not 0).
    with open(args.file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            # I remove trailing newline characters and prefix the line with its line number (e.g., "1: Kafka moves...").
            clean_line = line.rstrip('\r\n')
            value = f'{line_num}: {clean_line}'
            while True:
                try:
                    # I queue the numbered message into Kafka.
                    producer.produce(args.topic, key=key, value=value, callback=on_delivery)
                    break
                except BufferError:
                    # If the local producer buffer is full, I wait 1 second and retry.
                    producer.poll(1)
            count += 1
            # Let the client process any delivery callbacks without blocking.
            producer.poll(0)

    # Wait until every queued message is delivered before exiting.
    producer.flush()
    print(f'Sent {count - failed} of {count} numbered lines from {args.file} to topic {args.topic}')


if __name__ == '__main__':
    main()
