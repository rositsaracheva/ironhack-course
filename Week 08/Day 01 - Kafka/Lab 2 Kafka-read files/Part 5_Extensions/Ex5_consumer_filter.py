# Lab 2 — Part 5, Exercise 5: Filtering (--contains) — Consumer
# Student: Rositsa Kaloyanova
# Purpose: Read messages from a Kafka topic and write ONLY the lines that contain
#          the word passed via the --contains command-line option.

import argparse
import time

from confluent_kafka import Consumer


def main():
    # I set up command-line arguments, adding a new --contains option for filtering lines.
    parser = argparse.ArgumentParser(description='Write only matching lines from a Kafka topic to a file')
    parser.add_argument('--topic', default='ext5-filter')
    parser.add_argument('--out', default='ex5_filtered.txt')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument('--idle', type=int, default=5,
                        help='stop after this many seconds without messages')
    parser.add_argument('--group', default=f'ext5-consumer-{int(time.time())}')
    # New option: if I pass --contains topics, only lines containing "topics" will be written to the output file.
    parser.add_argument('--contains', default=None,
                        help='only write lines that contain this word (case-insensitive)')
    args = parser.parse_args()

    # I connect the Consumer to Kafka and start from the earliest message for this new group.
    consumer = Consumer({
        'bootstrap.servers': args.bootstrap,
        'group.id': args.group,
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe([args.topic])

    # I track both total messages read and how many matched the filter so I can show both in my summary.
    total_read = 0
    written = 0
    last_message = time.time()
    try:
        with open(args.out, 'w', encoding='utf-8', newline='\n') as out:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    if time.time() - last_message > args.idle:
                        break
                    continue
                if msg.error():
                    print(f'Consumer error: {msg.error()}')
                    continue

                # Decode the message bytes into UTF-8 text and reset the idle timer.
                text = msg.value().decode('utf-8')
                total_read += 1
                last_message = time.time()

                # If --contains was provided, I check (case-insensitively) whether the word appears in this line.
                # If it does NOT match, I skip writing this line and move on to the next message.
                if args.contains and args.contains.lower() not in text.lower():
                    continue

                # This line matched the filter (or no filter was set), so I write it to the output file.
                out.write(text + '\n')
                written += 1
    except KeyboardInterrupt:
        pass
    finally:
        # Always close the consumer cleanly to leave the consumer group.
        consumer.close()

    print(f'Read {total_read} lines, wrote {written} matching lines (filter="{args.contains}") to {args.out}')


if __name__ == '__main__':
    main()
