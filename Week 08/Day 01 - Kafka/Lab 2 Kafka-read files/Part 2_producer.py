# Lab 2 — Part 2: Custom Kafka Producer (producer.py)
# Student: Rositsa Kaloyanova
# Purpose: Read a text file line by line and send each line as one message to a Kafka topic.

# I import argparse so I can pass arguments from the terminal (like the file name and topic name).
import argparse
# I import os so I can extract just the file name (without the full folder path) to use as the message key.
import os

# I import the Producer class from the confluent_kafka library to connect to Kafka and send messages.
from confluent_kafka import Producer


def main():
    # I create an ArgumentParser to define the command-line inputs my script accepts.
    parser = argparse.ArgumentParser(description='Send a text file to Kafka')
    # Required positional argument: the path of the text file I want to send (for example, sample.txt).
    parser.add_argument('file', help='path of the text file to send')
    # Optional argument: the Kafka topic to send messages to (defaults to 'file-topic' if I don't specify one).
    parser.add_argument('--topic', default='file-topic')
    # Optional argument: the Kafka broker address (defaults to my local Docker Kafka broker at localhost:9092).
    parser.add_argument('--bootstrap', default='localhost:9092')
    # Parse all arguments typed in the terminal and store them in the args object.
    args = parser.parse_args()

    # I create a Kafka Producer client and tell it where the Kafka broker is running ('bootstrap.servers').
    producer = Producer({'bootstrap.servers': args.bootstrap})
    # I grab just the file name (e.g., 'sample.txt') to use as the Kafka message key.
    # Using the same key for every line guarantees that all lines go to the same partition and stay in order.
    key = os.path.basename(args.file)
    # I keep a counter to track how many messages failed to be delivered.
    failed = 0

    # This callback function is automatically called by Kafka once it knows whether a message succeeded or failed.
    def on_delivery(err, msg):
        # nonlocal lets this inner function update the 'failed' variable defined in main().
        nonlocal failed
        # If err is not None, something went wrong delivering the message, so I increment failed and print the error.
        if err is not None:
            failed += 1
            print(f'Delivery failed: {err}')

    # I keep a counter for the total number of lines I read from the file.
    count = 0
    # I open the text file in read mode ('r') using UTF-8 encoding so special characters are read safely.
    with open(args.file, 'r', encoding='utf-8') as f:
        # I loop through the file one line at a time so each line becomes one Kafka message.
        for line in f:
            # I strip the trailing newline characters ('\r' and '\n') so I send clean text without extra line breaks.
            value = line.rstrip('\r\n')
            # I use a while True loop so if the producer's local buffer fills up, I can pause and retry the same line.
            while True:
                try:
                    # produce() adds the message (topic, key, value) to the producer's internal queue and returns right away.
                    # I pass callback=on_delivery so I get notified if delivery fails.
                    producer.produce(args.topic, key=key, value=value,
                                     callback=on_delivery)
                    # If queuing succeeded, I break out of the retry loop and move on to the next line.
                    break
                except BufferError:
                    # If the local queue is full (for example, with a very large file), I wait up to 1 second
                    # with poll(1) to let Kafka drain some queued messages, then try again.
                    producer.poll(1)
            # I increase my line counter by 1 for every line queued.
            count += 1
            # poll(0) checks for delivery reports right away without blocking, triggering on_delivery if ready.
            producer.poll(0)

    # flush() waits until every single queued message has actually been delivered to Kafka.
    # Without flush(), the script might finish and exit before the last lines leave the queue!
    producer.flush()
    # I print a clear summary showing how many lines were successfully sent out of the total lines read.
    print(f'Sent {count - failed} of {count} lines from {args.file} to topic {args.topic}')


# This standard Python check ensures main() only runs when I execute this file directly from the terminal.
if __name__ == '__main__':
    main()
