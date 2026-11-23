# Lab 2 — Part 5: Extension Exercises

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`) + Python (`confluent-kafka`)

---

## Exercise 1 — Line Numbers ✅

**Goal:** Make the producer prefix each message with its line number, and have the consumer print the line numbers on screen.

### What I Changed
- **Producer ([Ex1_producer_line_numbers.py](Ex1_producer_line_numbers.py)):** Used `enumerate(f, start=1)` to number each line starting at 1 and format the message value as `f'{line_num}: {clean_line}'`.
- **Consumer ([Ex1_consumer_line_numbers.py](Ex1_consumer_line_numbers.py)):** Extracted the line number prefix using `text.split(':', 1)[0]` and printed `Received line #<line_num>` on screen while writing each line to [ex1_received.txt](ex1_received.txt).

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext1-line-numbers --bootstrap-server localhost:9092
python3 Ex1_producer_line_numbers.py ../sample.txt --topic ext1-line-numbers
python3 Ex1_consumer_line_numbers.py --topic ext1-line-numbers --out ex1_received.txt --idle 4
```
```text
Sent 5 of 5 numbered lines from ../sample.txt to topic ext1-line-numbers
Received line #1
Received line #2
Received line #3
Received line #4
Received line #5
Wrote 5 lines to ex1_received.txt
```

---

## Exercise 2 — Several Files ✅

**Goal:** Send two different files to the same topic. Since the message key already holds the file name, make the consumer write one output file per key.

### What I Changed
- **Producer:** Reused [../Part 2_producer.py](../Part%202_producer.py) directly because it already sets `key = os.path.basename(args.file)`.
- **Consumer ([Ex2_consumer_several_files.py](Ex2_consumer_several_files.py)):** Read `msg.key().decode('utf-8')` for each incoming message, kept a dictionary (`open_files`) mapping each key to its own output file (`out_<key>`), wrote each message to its matching file, and closed all open files in `finally`.

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext2-several-files --bootstrap-server localhost:9092
python3 "../Part 2_producer.py" ex2_fileA.txt --topic ext2-several-files
python3 "../Part 2_producer.py" ex2_fileB.txt --topic ext2-several-files
python3 Ex2_consumer_several_files.py --topic ext2-several-files --idle 4
diff ex2_fileA.txt out_ex2_fileA.txt
diff ex2_fileB.txt out_ex2_fileB.txt
```
```text
Sent 3 of 3 lines from ex2_fileA.txt to topic ext2-several-files
Sent 3 of 3 lines from ex2_fileB.txt to topic ext2-several-files
Wrote 3 lines to out_ex2_fileA.txt (key=ex2_fileA.txt)
Wrote 3 lines to out_ex2_fileB.txt (key=ex2_fileB.txt)
```
- **Verified:** Both [out_ex2_fileA.txt](out_ex2_fileA.txt) and [out_ex2_fileB.txt](out_ex2_fileB.txt) matched [ex2_fileA.txt](ex2_fileA.txt) and [ex2_fileB.txt](ex2_fileB.txt) with `diff` returning 0 differences!

---

## Exercise 3 — Only New Messages ✅

**Goal:** Run the consumer twice with the same `--group demo`. The second run should write only lines sent after the first run finished.

### Why This Works
- No code changes were needed — I reused [../Part 2_producer.py](../Part%202_producer.py) and [../Part 3_consumer.py](../Part%203_consumer.py).
- Because both runs used the **same consumer group (`--group demo`)**, Kafka saved the committed offset after Run 1 finished (when `consumer.close()` ran). When Run 2 started with `--group demo`, Kafka resumed from that saved offset instead of re-reading from the beginning, so Run 2 only received the new messages from Batch 2!

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext3-demo-topic --bootstrap-server localhost:9092

# Batch 1 + Consumer Run 1
python3 "../Part 2_producer.py" ex3_batch1.txt --topic ext3-demo-topic
python3 "../Part 3_consumer.py" --topic ext3-demo-topic --group demo --out ex3_run1.txt --idle 6

# Batch 2 + Consumer Run 2 (same --group demo!)
python3 "../Part 2_producer.py" ex3_batch2.txt --topic ext3-demo-topic
python3 "../Part 3_consumer.py" --topic ext3-demo-topic --group demo --out ex3_run2.txt --idle 6
```
```text
Sent 2 of 2 lines from ex3_batch1.txt to topic ext3-demo-topic
Wrote 2 lines to ex3_run1.txt
Sent 2 of 2 lines from ex3_batch2.txt to topic ext3-demo-topic
Wrote 2 lines to ex3_run2.txt
```
- **[ex3_run1.txt](ex3_run1.txt):** Contains only the 2 lines from [ex3_batch1.txt](ex3_batch1.txt).
- **[ex3_run2.txt](ex3_run2.txt):** Contains only the 2 new lines from [ex3_batch2.txt](ex3_batch2.txt) (`diff` confirmed 0 differences for both!).

---

## Exercise 4 — End Marker (`__EOF__`) ✅

**Goal:** Have the producer send a final message such as `__EOF__`, and make the consumer stop the moment it sees it instead of waiting for the idle timer.

### What Is `__EOF__`?
- **EOF** stands for **End Of File**. Because a Kafka topic is a continuous stream, the consumer normally doesn't know if the file is finished or if more lines are still coming (which is why it previously had to wait out the `--idle` timer). Sending a special `__EOF__` marker right after the last line tells the consumer that the file is complete so it can stop immediately.

### What I Changed
- **Producer ([Ex4_producer_eof.py](Ex4_producer_eof.py)):** After sending all lines of the file, queues one extra message with value `'__EOF__'` and the same message key so it arrives right after the last line in the same partition.
- **Consumer ([Ex4_consumer_eof.py](Ex4_consumer_eof.py)):** Checks `if text == '__EOF__': break` before writing to the file, so it exits immediately without writing `__EOF__` into [ex4_received.txt](ex4_received.txt) and without waiting out `--idle 30`.

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext4-eof --bootstrap-server localhost:9092
python3 Ex4_producer_eof.py ../sample.txt --topic ext4-eof
python3 Ex4_consumer_eof.py --topic ext4-eof --out ex4_received.txt --idle 30
diff ../sample.txt ex4_received.txt
```
```text
Sent 5 of 5 lines + __EOF__ marker from ../sample.txt to topic ext4-eof
End marker (__EOF__) received — stopping immediately!
Wrote 5 lines to ex4_received.txt
```
- **Verified:** Stopped immediately on `__EOF__` (instead of waiting 30 seconds) and `diff` confirmed 0 differences between `../sample.txt` and [ex4_received.txt](ex4_received.txt)!

---

## Exercise 5 — Filtering (`--contains`) ✅

**Goal:** Make the consumer write only lines that contain a word given with a `--contains` option.

### What I Changed
- **Producer:** Reused [../Part 2_producer.py](../Part%202_producer.py) to send `../sample.txt` (5 lines).
- **Consumer ([Ex5_consumer_filter.py](Ex5_consumer_filter.py)):** Added a `--contains` command-line argument and checked `if args.contains and args.contains.lower() not in text.lower(): continue` so only matching lines are written to [ex5_filtered.txt](ex5_filtered.txt).
- **Note on `--idle 5`:** `--idle` sets the consumer's wait timer in seconds. Passing `--idle 5` tells the consumer to stop automatically after 5 seconds with no new messages (instead of waiting the default 10 seconds), so it finishes faster once all messages have been read.

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext5-filter --bootstrap-server localhost:9092
python3 "../Part 2_producer.py" ../sample.txt --topic ext5-filter
python3 Ex5_consumer_filter.py --topic ext5-filter --contains topics --out ex5_filtered.txt --idle 5
```
```text
Sent 5 of 5 lines from ../sample.txt to topic ext5-filter
Read 5 lines, wrote 2 matching lines (filter="topics") to ex5_filtered.txt
```
- **[ex5_filtered.txt](ex5_filtered.txt) contents (only the 2 lines containing `"topics"`):**
```text
Producers write to topics.
Consumers read from topics.
```

---

## Exercise 6 — Larger Files (100,000 Lines Benchmark) ✅

**Goal:** Generate a file with 100,000 lines and time how long the producer takes to send all of them to Kafka.

### What I Built
- **[Ex6_benchmark_large_file.py](Ex6_benchmark_large_file.py):** Generates a 100,000-line file ([ex6_large_100k.txt](ex6_large_100k.txt), ~4.0 MB) and times [../Part 2_producer.py](../Part%202_producer.py) sending all 100,000 lines to topic `ext6-large-file` using `time.perf_counter()`.

### Commands & Verified Output
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic ext6-large-file --bootstrap-server localhost:9092
python3 Ex6_benchmark_large_file.py
```
```text
Generating ex6_large_100k.txt with 100,000 lines...
Finished generating ex6_large_100k.txt.
Sent 100000 of 100000 lines from ex6_large_100k.txt to topic ext6-large-file
Elapsed time: 0.25 seconds (405,793 messages/second)
```
- **Takeaway:** Sending **100,000 lines (4.0 MB)** took only **0.25 seconds** (~**405,793 messages/second**) because `confluent-kafka` batches messages asynchronously in C (`librdkafka`) and Kafka appends them sequentially to the partition log!
