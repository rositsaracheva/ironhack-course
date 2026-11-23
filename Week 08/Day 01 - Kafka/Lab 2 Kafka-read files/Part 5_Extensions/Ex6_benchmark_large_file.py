# Lab 2 — Part 5, Exercise 6: Larger Files (100,000 Lines Benchmark)
# Student: Rositsa Kaloyanova
# Purpose: Generate a 100,000-line text file and measure how fast Part 2_producer.py sends all 100,000 messages to Kafka.

import subprocess
import sys
import time

# I set the number of lines to 100,000, the output file name, and the Kafka topic name.
NUM_LINES = 100_000
LARGE_FILE = 'ex6_large_100k.txt'
TOPIC = 'ext6-large-file'


def main():
    # Step 1: Generate a text file with 100,000 lines.
    print(f'Generating {LARGE_FILE} with {NUM_LINES:,} lines...')
    with open(LARGE_FILE, 'w', encoding='utf-8', newline='\n') as f:
        for i in range(1, NUM_LINES + 1):
            f.write(f'Line {i}: Kafka throughput test message\n')
    print(f'Finished generating {LARGE_FILE}.')

    # Step 2: Start a high-precision timer and run Part 2_producer.py to send all 100,000 lines to Kafka.
    # This also exercises the BufferError / poll(1) retry logic in Part 2_producer.py!
    start = time.perf_counter()
    subprocess.run(
        [sys.executable, '../Part 2_producer.py', LARGE_FILE, '--topic', TOPIC],
        check=True,
    )
    elapsed = time.perf_counter() - start

    # Step 3: Calculate and print the total time and throughput (messages per second).
    rate = NUM_LINES / elapsed if elapsed > 0 else 0
    print(f'Elapsed time: {elapsed:.2f} seconds ({rate:,.0f} messages/second)')


if __name__ == '__main__':
    main()
