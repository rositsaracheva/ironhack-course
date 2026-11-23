# Lab 2 — Part 3: The Consumer (`Part 3_consumer.py`)

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`) + Python (`confluent-kafka`)  
**Code File:** [Part 3_consumer.py](Part%203_consumer.py)

---

## Goal

Write a custom Kafka consumer in Python that reads messages from a Kafka topic (`file-topic`) and writes each message back as a line in an output text file (`received.txt`).

---

## How `Part 3_consumer.py` Works

1. **Command-line arguments (`argparse`):**
   - Accepts `--topic` (default `file-topic`), `--out` (default `received.txt`), `--bootstrap` (default `localhost:9092`), `--idle` (default `10` seconds), and `--group` (default `file-consumer-<current_timestamp>`).
2. **Consumer group & offsets (`group.id` + `auto.offset.reset: 'earliest'`):**
   - `group.id` names the consumer group so Kafka can track which offsets this group has already read. Adding the current timestamp by default means every run starts as a brand-new group.
   - `auto.offset.reset: 'earliest'` tells a new consumer group to start at offset 0 (the very first message in the topic).
3. **Subscribing & polling (`subscribe()` + `poll(1.0)`):**
   - `consumer.subscribe([args.topic])` subscribes to the target topic.
   - Inside the loop, `consumer.poll(1.0)` waits up to 1 second for a message and returns `None` if nothing arrives.
4. **Idle timer (`--idle`):**
   - Tracks the timestamp of the last received message (`last_message`). If more than `--idle` seconds pass with no new messages, the loop breaks automatically so the script finishes cleanly (you can also press `Ctrl-C` anytime).
5. **Decoding & writing (`msg.value().decode('utf-8')`):**
   - Kafka messages arrive as raw bytes, so the consumer decodes each message as UTF-8 text and writes it with `\n` to the output file.
6. **Clean shutdown (`finally: consumer.close()`):**
   - Putting `consumer.close()` inside a `finally` block guarantees the consumer commits its offsets and leaves the consumer group cleanly — even if stopped early with `Ctrl-C`.

---

## Verification ✅

```bash
python3 -m py_compile "Part 3_consumer.py"
python3 "Part 3_consumer.py" --help
```
- **Verified:** Syntax compiled cleanly and CLI options (`--topic`, `--out`, `--bootstrap`, `--idle`, `--group`) worked without errors.
