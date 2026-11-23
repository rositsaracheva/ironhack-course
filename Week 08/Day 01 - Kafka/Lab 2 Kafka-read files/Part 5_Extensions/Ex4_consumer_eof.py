# Lab 2 — Part 5, Exercise 4: End Marker (__EOF__) — Consumer
# Student: Rositsa Kaloyanova
# Purpose: Read lines from Kafka into an output file and stop the instant '__EOF__' arrives,
#          instead of waiting out the idle timer.

import argparse
import time

from confluent_kafka import Consumer

# Must match the exact end marker sent by Ex4_producer_eof.py.
EOF_MARKER = '__EOF__'


def main():
    # I set up command-line arguments (note: --idle is still kept as a safety fallback if __EOF__ never arrives).
    parser = argparse.ArgumentParser(description='Write a Kafka topic to a file and stop on __EOF__')
    parser.add_argument('--topic', default='ext4-eof')
    parser.add_argument('--out', default='ex4_received.txt')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument('--idle', type=int, default=30,
                        help='safety timeout if __EOF__ never arrives')
    parser.add_argument('--group', default=f'ext4-consumer-{int(time.time())}')
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
                msg = consumer.poll(1.0)
                if msg is None:
                    if time.time() - last_message > args.idle:
                        break
                    continue
                if msg.error():
                    print(f'Consumer error: {msg.error()}')
                    continue

                # I decode the message value from bytes to UTF-8 text.
                text = msg.value().decode('utf-8')
                # If the message is our special '__EOF__' marker, I stop immediately
                # without writing '__EOF__' into the output file and without waiting for --idle!
                if text == EOF_MARKER:
                    print(f'End marker ({EOF_MARKER}) received — stopping immediately!')
                    break

                # Otherwise, it is a normal file line, so I write it to the output file.
                out.write(text + '\n')
                count += 1
                last_message = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        # Always close the consumer cleanly to leave the group.
        consumer.close()

    print(f'Wrote {count} lines to {args.out}')


if __name__ == '__main__':
    main()
