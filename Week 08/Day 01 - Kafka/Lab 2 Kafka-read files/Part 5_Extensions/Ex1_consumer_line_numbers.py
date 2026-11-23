# Lab 2 — Part 5, Exercise 1: Line Numbers — Consumer
# Student: Rositsa Kaloyanova
# Purpose: Read numbered messages from Kafka, print each line number on screen, and write the lines to a file.

import argparse
import time

from confluent_kafka import Consumer


def main():
    # I define the command-line options for topic, output file, broker, idle timeout, and consumer group.
    parser = argparse.ArgumentParser(description='Read numbered lines from Kafka and print line numbers')
    parser.add_argument('--topic', default='ext1-line-numbers')
    parser.add_argument('--out', default='ex1_received.txt')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument('--idle', type=int, default=5,
                        help='stop after this many seconds without messages')
    parser.add_argument('--group', default=f'ext1-consumer-{int(time.time())}')
    args = parser.parse_args()

    # I connect the Consumer to Kafka and start from the earliest message for this new group.
    consumer = Consumer({
        'bootstrap.servers': args.bootstrap,
        'group.id': args.group,
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe([args.topic])

    count = 0
    last_message = time.time()
    try:
        with open(args.out, 'w', encoding='utf-8', newline='\n') as out:
            while True:
                # Poll Kafka for up to 1 second waiting for the next message.
                msg = consumer.poll(1.0)
                if msg is None:
                    if time.time() - last_message > args.idle:
                        break
                    continue
                if msg.error():
                    print(f'Consumer error: {msg.error()}')
                    continue

                # I decode the message bytes into a UTF-8 string (format: "<line_num>: <text>").
                text = msg.value().decode('utf-8')
                # I split once on ': ' to extract the line number prefix and print it on screen.
                line_num = text.split(':', 1)[0]
                print(f'Received line #{line_num}')

                # I write the full received line to the output file and update my counter/timer.
                out.write(text + '\n')
                count += 1
                last_message = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        # Always close the consumer cleanly to leave the consumer group.
        consumer.close()

    print(f'Wrote {count} lines to {args.out}')


if __name__ == '__main__':
    main()
