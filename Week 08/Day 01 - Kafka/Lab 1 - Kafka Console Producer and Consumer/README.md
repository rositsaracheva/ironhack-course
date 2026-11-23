# Week 08 — Day 01: Lab 1 — Kafka Console Producer and Consumer

**Student:** Rositsa Kaloyanova
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`)
**Submission:** even though we are currently in Week 08. This Lab 1 will be submitted in Week 7 / Day 4 as instructed by the teacher.



---

## 🎯 Lab Notes:

In this lab, I ran Apache Kafka inside a Docker container and used Kafka's built-in console tools (`kafka-topics.sh`, `kafka-console-producer.sh`, and `kafka-console-consumer.sh`) to:

1. Launch a single-broker Kafka container in Docker (`apache/kafka:latest`)
2. Create, list, and inspect Kafka topics (`lab1-topic`, `Monday`, `files-console`)
3. Stream live messages from a Producer to a Consumer and replay them using `--from-beginning`
4. Pipe an entire text file (`data.txt`) through Kafka into a new file (`received.txt`) and verify 100% integrity with `diff`

---

## ⚙️ Prerequisite: Start Apache Kafka in Docker

```bash
# Launch the official Apache Kafka container in detached mode (-d) on port 9092
docker run -d --name kafka -p 9092:9092 apache/kafka:latest

# Verify the container is running
docker ps
```

---

## 📌 Part 1: Create, List, and Describe a Topic (`lab1-topic`)

1. **Create the topic `lab1-topic`:**

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic lab1-topic --bootstrap-server localhost:9092
   ```

   - **Result:** `Created topic lab1-topic.`
2. **List all topics:**

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
   ```
3. **Describe `lab1-topic`:**

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --describe --topic lab1-topic --bootstrap-server localhost:9092
   ```

   - **Checkpoint Verified:** Shows `PartitionCount: 1` and `ReplicationFactor: 1` (default settings for a single-broker Docker setup).

---

## 💬 Part 2: Console Producer, Consumer & Replay (`lab1-topic` & `Monday`)

1. **Window A — Start the live Consumer (listener):**

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic lab1-topic --bootstrap-server localhost:9092
   ```
2. **Window B — Start the live Producer (sender) and type 3 messages:**

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic lab1-topic --bootstrap-server localhost:9092
   ```

   Messages sent:

   ```text
   hello kafka
   this is my second message
   this is my third message
   ```
3. **Replay the whole topic from the beginning (`--from-beginning`):**
   Because Kafka retains messages after they are read (unlike traditional queues), starting a new consumer with `--from-beginning` replays all stored messages in order:

   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic lab1-topic --from-beginning --max-messages 3 --bootstrap-server localhost:9092
   ```

   - **Verified Output:**
     ```text
     hello kafka
     this is my second message
     this is my third message
     Processed a total of 3 messages
     ```
4. **Class Demo Topic (`Monday`):**
   Created topic `Monday`, produced 9 live chat messages (`hello we are`, `learning`, `Apache Kafka`, `this`, `is`, `a`, `live`, `chat`, `bot`), and verified all 9 messages with `--from-beginning --max-messages 9`.

---

## 📄 Part 3: Send a Text File Through Kafka (Adapted for macOS Terminal)

Since the lab handout uses Windows PowerShell commands (`Set-Content`, `Get-Content`, `Out-File`, `Compare-Object`), I adapted each step to native **macOS (`zsh`)** commands:

### Step 1 — Create a fresh topic (`files-console`)

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic files-console --bootstrap-server localhost:9092
```

- **Output:** `Created topic files-console.`

### Step 2 — Create the sample input file (`data.txt`)

*(macOS equivalent of PowerShell's `Set-Content`)*

```bash
printf "first line\nsecond line\nthird line\nfourth line\n" > data.txt
cat data.txt
```

- **File created:** [data.txt](data.txt) (4 lines)

### Step 3 — Pipe `data.txt` into the Kafka Console Producer

*(macOS equivalent of PowerShell's `Get-Content`; uses `-i` instead of `-it` because stdin is piped)*

```bash
cat data.txt | docker exec -i kafka /opt/kafka/bin/kafka-console-producer.sh --topic files-console --bootstrap-server localhost:9092
```

- Each line in `data.txt` is sent into Kafka as an individual message (4 messages total).

### Step 4 — Consume the messages from Kafka into `received.txt`

*(macOS equivalent of PowerShell's `Out-File -Encoding utf8`; `--max-messages 4` exits cleanly once all 4 messages are received)*

```bash
docker exec kafka /opt/kafka/bin/kafka-console-consumer.sh --topic files-console --from-beginning --max-messages 4 --bootstrap-server localhost:9092 > received.txt
cat received.txt
```

- **File created:** [received.txt](received.txt)
- **Verified Output:**
  ```text
  first line
  second line
  third line
  fourth line
  ```

### Step 5 — Compare `data.txt` and `received.txt`

*(macOS equivalent of PowerShell's `Compare-Object`)*

```bash
diff data.txt received.txt
```

- **Checkpoint Verified:** `diff` returned **empty output (exit code 0)**, confirming that `data.txt` and `received.txt` match line-for-line with 100% fidelity! ✅

---

## 📁 Files in This Folder

- **[README.md](README.md)** — Complete step-by-step documentation of Parts 1, 2, and 3 (including macOS adaptations and verified outputs).
- **[data.txt](data.txt)** — Original 4-line input text file sent into Kafka topic `files-console`.
- **[received.txt](received.txt)** — 4-line output file consumed from Kafka topic `files-console`.
- **[Lab 1 Kafka Console Producer and Consumer.docx.pdf](Lab%201%20Kafka%20Console%20Producer%20and%20Consumer.docx.pdf)** — Official lab instructions.
