# Lab 2 — Part 4: Run the Lab and Verify

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`) + Python (`confluent-kafka`)

---

## Steps Completed & Verified ✅

### 1. Send `sample.txt` to Kafka (`file-topic`)
```bash
python3 "Part 2_producer.py" sample.txt --topic file-topic
```
- **Output:**
```text
Sent 5 of 5 lines from sample.txt to topic file-topic
```

### 2. Receive Messages into `received.txt`
```bash
python3 "Part 3_consumer.py" --topic file-topic --out received.txt
```
- **Output:**
```text
Wrote 5 lines to received.txt
```
- **File created:** [received.txt](received.txt) (5 lines)

### 3. Compare `sample.txt` and `received.txt`
*(macOS `zsh` equivalent of PowerShell's `Compare-Object`)*
```bash
diff sample.txt received.txt
```
- **Checkpoint Verified:** `diff` returned **empty output (0 differences)** — [sample.txt](sample.txt) and [received.txt](received.txt) match line-for-line! ✅

---

## Try It Live (`live.txt`)

To test receiving both earlier retained messages and newly produced messages:

1. **Send `sample.txt` a second time to `file-topic`:**
   ```bash
   python3 "Part 2_producer.py" sample.txt --topic file-topic
   ```
   - **Output:** `Sent 5 of 5 lines from sample.txt to topic file-topic`

2. **Consume into `live.txt`:**
   ```bash
   python3 "Part 3_consumer.py" --topic file-topic --out live.txt --idle 60
   ```
   - **Output:** `Wrote 10 lines to live.txt`
   - **File created:** [live.txt](live.txt) (**10 lines** total — the 5 earlier retained messages plus the 5 new messages, because each run uses a new timestamp-based `--group` with `auto.offset.reset: 'earliest'`).
