# Lab 2 — Part 2: The Producer (`Part 2_producer.py`)

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`) + Python (`confluent-kafka`)  
**Code File:** [Part 2_producer.py](Part%202_producer.py)

---

## Goal

Write a custom Kafka producer in Python that reads a text file line by line and sends each line as one message to a Kafka topic (`file-topic`).

---

## How `Part 2_producer.py` Works

1. **Command-line arguments (`argparse`):**
   - Takes the path of the input text file (`file`, e.g., `sample.txt`), plus optional `--topic` (default `file-topic`) and `--bootstrap` (default `localhost:9092`).
2. **Connecting to Kafka (`Producer({'bootstrap.servers': args.bootstrap})`):**
   - Creates a Kafka Producer client that talks to my local Docker Kafka broker at `localhost:9092`.
3. **Message key (`key = os.path.basename(args.file)`):**
   - Uses just the file name (`sample.txt`) as the Kafka message key. Messages with the same key always go to the **same partition**, so all lines arrive in their exact original order.
4. **Delivery callback (`on_delivery(err, msg)`):**
   - Kafka calls this function once it knows whether a message succeeded or failed. If `err` is not `None`, it increments `failed` and prints the error.
5. **Streaming line by line (`produce()`, `poll(0)`, and `BufferError`):**
   - Opens the file in UTF-8 (`with open(args.file, 'r', encoding='utf-8')`), strips trailing `\r\n`, and queues each line with `producer.produce(...)`.
   - `poll(0)` checks for delivery reports without blocking.
   - If the local queue fills up (for example, on a very large file), catching `BufferError` pauses briefly with `producer.poll(1)` so Kafka can drain the queue, then retries the same line.
6. **Waiting for completion (`producer.flush()`):**
   - Blocks until every queued message has actually been delivered to Kafka before the script exits and prints the summary (`Sent X of Y lines...`).

---

## Verification ✅

```bash
python3 -m py_compile "Part 2_producer.py"
python3 "Part 2_producer.py" --help
```
- **Verified:** Syntax compiled cleanly and CLI options (`file`, `--topic`, `--bootstrap`) worked without errors.
