# Lab 2 — Part 1: Set up

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`) + Python (`confluent-kafka`)

---

## Steps Completed & Verified ✅

### 1. Start and Confirm the Kafka Docker Container
```bash
docker start kafka
docker ps
```
- **Verified:** The `kafka` container (`apache/kafka:latest`) is running on `localhost:9092`.

### 2. Check Python Version
```bash
python3 --version
```
- **Verified:** `Python 3.14.6` (`/opt/anaconda3/bin/python3`).

### 3. Install the Kafka Client Library for Python (`confluent-kafka`)
```bash
python3 -m pip install confluent-kafka
```
- **Verified:** Installed `confluent-kafka` (`2.16.2`) with zero errors.

### 4. Create the Kafka Topic (`file-topic`)
```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic file-topic --bootstrap-server localhost:9092
```
- **Result:** `Created topic file-topic.`

### 5. Create the Sample File to Transfer (`sample.txt`)
*(macOS `zsh` equivalent of PowerShell's `Set-Content`)*
```bash
printf "Kafka moves messages between programs.\nEach line of this file is one message.\nProducers write to topics.\nConsumers read from topics.\nThis is the last line.\n" > sample.txt
```
- **File created:** [sample.txt](sample.txt)
- **Contents (5 lines):**
```text
Kafka moves messages between programs.
Each line of this file is one message.
Producers write to topics.
Consumers read from topics.
This is the last line.
```
