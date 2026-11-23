# Lab 2 — Part 5, Exercise 2: Several Files — Consumer
# Student: Rositsa Kaloyanova
# Purpose: Read messages from a single Kafka topic that contains multiple files, and use each
#          message's key (the original file name) to write one separate output file per key.

import argparse
import os
import time

from confluent_kafka import Consumer


def main():
    # I set up command-line arguments for the topic, output filename prefix, broker, idle timeout, and group.
    parser = argparse.ArgumentParser(description='Write one output file per Kafka message key')
    parser.add_argument('--topic', default='ext2-several-files')
    parser.add_argument('--prefix', default='out_',
                        help='prefix added to each key so I do not overwrite the original input files')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument('--idle', type=int, default=4,
                        help='stop after this many seconds without messages')
    parser.add_argument('--group', default=f'ext2-consumer-{int(time.time())}')
    args = parser.parse_args()

    # I connect to the local Kafka broker and start from the earliest message for this new consumer group.
    consumer = Consumer({
        'bootstrap.servers': args.bootstrap,
        'group.id': args.group,
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe([args.topic])

    # I use a dictionary to keep track of each output file I have opened, keyed by the message key (file name).
    open_files = {}
    # I also track how many lines were written to each file so I can print a nice summary at the end.
    counts = {}
    last_message = time.time()

    try:
        while True:
            # Wait up to 1 second for the next message from Kafka.
            msg = consumer.poll(1.0)
            if msg is None:
                if time.time() - last_message > args.idle:
                    break
                continue
            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue

            # I read the message key (which holds the file name sent by the producer).
            # If a message has no key, I fall back to 'unknown.txt'.
            raw_key = msg.key()
            key_name = os.path.basename(raw_key.decode('utf-8')) if raw_key else 'unknown.txt'

            # If this is the first time I see this key, I open a new output file for it (e.g., out_ex2_fileA.txt).
            if key_name not in open_files:
                out_path = f'{args.prefix}{key_name}'
                open_files[key_name] = open(out_path, 'w', encoding='utf-8', newline='\n')
                counts[key_name] = 0

            # I decode the message value from bytes to UTF-8 text and write it to the matching file.
            open_files[key_name].write(msg.value().decode('utf-8') + '\n')
            counts[key_name] += 1
            last_message = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        # I make sure every opened output file is closed properly, even if I stop the script with Ctrl-C.
        for f in open_files.values():
            f.close()
        # I close the Kafka consumer cleanly to leave the consumer group.
        consumer.close()

    # I print a summary showing how many lines were written to each output file.
    for key_name, line_count in counts.items():
        print(f'Wrote {line_count} lines to {args.prefix}{key_name} (key={key_name})')


if __name__ == '__main__':
    main()
