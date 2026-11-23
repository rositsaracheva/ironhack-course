# Lab 2 — Part 3: Custom Kafka Consumer (Part 3_consumer.py)
# Student: Rositsa Kaloyanova
# Purpose: Read messages from a Kafka topic and write each message as a line in an output text file.

# I import argparse so I can pass options from the terminal (topic, output file, idle timeout, consumer group).
import argparse
# I import time so I can track how many seconds have passed since the last message (and build a unique group name).
import time

# I import the Consumer class from confluent_kafka to connect to Kafka and read messages.
from confluent_kafka import Consumer


def main():
    # I create an ArgumentParser to define the command-line options for my consumer script.
    parser = argparse.ArgumentParser(description='Write a Kafka topic to a file')
    # Optional argument: which Kafka topic to read from (defaults to 'file-topic').
    parser.add_argument('--topic', default='file-topic')
    # Optional argument: the output file path where received lines will be saved (defaults to 'received.txt').
    parser.add_argument('--out', default='received.txt')
    # Optional argument: the Kafka broker address (defaults to my local Docker Kafka broker at localhost:9092).
    parser.add_argument('--bootstrap', default='localhost:9092')
    # Optional argument: how many seconds of silence to wait before automatically stopping (defaults to 10 seconds).
    parser.add_argument('--idle', type=int, default=10,
                        help='stop after this many seconds without messages')
    # Optional argument: the consumer group ID. By default I attach the current timestamp so every run
    # creates a brand-new consumer group and reads the topic from the very beginning.
    parser.add_argument('--group', default=f'file-consumer-{int(time.time())}')
    # Parse the command-line arguments and store them in args.
    args = parser.parse_args()

    # I create the Kafka Consumer client with three key settings:
    # - 'bootstrap.servers': tells the consumer where to find the Kafka broker.
    # - 'group.id': names the consumer group so Kafka can track offsets for this group.
    # - 'auto.offset.reset': 'earliest' tells a new consumer group to start from the very first message in the topic.
    consumer = Consumer({
        'bootstrap.servers': args.bootstrap,
        'group.id': args.group,
        'auto.offset.reset': 'earliest',
    })
    # I subscribe this consumer to a list containing our target topic.
    consumer.subscribe([args.topic])

    # I keep a counter to track how many lines I write to the output file.
    count = 0
    # I record the current time so I can measure how long we have been waiting without receiving a message.
    last_message = time.time()
    # I wrap the reading loop in try/except/finally so the consumer always closes cleanly (even if I press Ctrl-C).
    try:
        # I open the output file in write mode ('w') with UTF-8 encoding and standard Unix '\n' line endings.
        with open(args.out, 'w', encoding='utf-8', newline='\n') as out:
            # I keep polling Kafka in a loop until the idle timer expires (or I press Ctrl-C).
            while True:
                # poll(1.0) waits up to 1 second for the next message from Kafka; if none arrives, it returns None.
                msg = consumer.poll(1.0)
                if msg is None:
                    # If no message arrived, I check whether we've waited longer than --idle seconds.
                    if time.time() - last_message > args.idle:
                        # Idle timeout reached, so I break out of the loop and finish cleanly.
                        break
                    # Otherwise, keep waiting in the next iteration of the loop.
                    continue
                # If Kafka returned an error object instead of a valid message, I print it and skip to the next poll.
                if msg.error():
                    print(f'Consumer error: {msg.error()}')
                    continue
                # msg.value() returns raw bytes, so I decode it as UTF-8 text and write it as a line in the output file.
                out.write(msg.value().decode('utf-8') + '\n')
                # I increment my counter for every line written.
                count += 1
                # I reset the idle timer because I just received a message.
                last_message = time.time()
    except KeyboardInterrupt:
        # If I press Ctrl-C in the terminal, I catch it gracefully instead of showing a messy traceback.
        pass
    finally:
        # close() commits final offsets and leaves the consumer group cleanly.
        # Putting it in finally guarantees it runs whether the script finishes normally or stops via Ctrl-C.
        consumer.close()

    # I print a summary of how many lines were written and where they were saved.
    print(f'Wrote {count} lines to {args.out}')


# This standard Python check makes sure main() only runs when I execute this file directly.
if __name__ == '__main__':
    main()
