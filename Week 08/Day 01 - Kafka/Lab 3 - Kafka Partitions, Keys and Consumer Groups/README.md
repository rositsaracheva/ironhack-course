# Week 08 — Day 01: Lab 3 — Kafka Partitions, Keys and Consumer Groups

**Student:** Rositsa Kaloyanova  
**Environment:** macOS Terminal (`zsh`) + Docker (`apache/kafka:latest`)  
**Lab Instructions:** [Lab 3 Kafka Partitions, Keys and Consumer Groups.docx.pdf](Lab%203%20Kafka%20Partitions,%20Keys%20and%20Consumer%20Groups.docx.pdf)

---

## 🎯 Lab Overview

In this lab, I used Kafka's console tools inside my Docker container (`kafka`) to explore the three core concepts that allow Apache Kafka to scale:
1. **Partitions** — splitting a topic into multiple ordered logs
2. **Message Keys & Ordering** — routing all events with the same key to the same partition so their order is guaranteed
3. **Consumer Groups** — sharing partitions across consumers in the same group, automatic failover when one consumer stops, and independent reading by a different consumer group

---

## ⚙️ Prerequisite: Start Apache Kafka in Docker

```bash
docker start kafka
docker ps
```
- **Verified:** Container `kafka` (`apache/kafka:latest`) running on `localhost:9092`.

---

## 📌 Part 1: Partitions

1. **Create the `orders` topic with 3 partitions:**
   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic orders --partitions 3 --bootstrap-server localhost:9092
   ```

2. **Describe `orders` to inspect its layout:**
   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
   ```

- **Checkpoint Verified:**
  ```text
  Topic: orders   PartitionCount: 3   ReplicationFactor: 1
    Topic: orders  Partition: 0  Leader: 1  Replicas: 1  Isr: 1
    Topic: orders  Partition: 1  Leader: 1  Replicas: 1  Isr: 1
    Topic: orders  Partition: 2  Leader: 1  Replicas: 1  Isr: 1
  ```
  *(ReplicationFactor is `1` and all 3 partitions share the same leader broker because this lab runs a single-broker Kafka container.)*

---

## 🔑 Part 2: Keys and Ordering

1. **Window A — Consumer printing partition and key:**
   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
   ```

2. **Window B — Producer parsing `key:message` pairs:**
   ```bash
   docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092 --property parse.key=true --property key.separator=:
   ```
   Messages sent:
   ```text
   user1:login
   user2:login
   user3:login
   user1:add-to-cart
   user2:add-to-cart
   user1:logout
   user3:logout
   user2:logout
   ```

3. **Verified Output (8 messages total):**
   ```text
   Partition:0  Offset:0  user1  login
   Partition:0  Offset:1  user1  add-to-cart
   Partition:0  Offset:2  user1  logout
   Partition:2  Offset:0  user2  login
   Partition:2  Offset:1  user3  login
   Partition:2  Offset:2  user2  add-to-cart
   Partition:2  Offset:3  user3  logout
   Partition:2  Offset:4  user2  logout
   ```

4. **Answers to Part 2 Questions:**
   - **Is every `user1` message in the same partition?** Yes — all 3 `user1` messages landed in **Partition 0**.
   - **Do all three users share one partition, or are they spread out?** They are **spread out** (`user1` hashed to Partition 0, while `user2` and `user3` hashed to Partition 2).
   - **For one user, do the messages appear in the order I typed them?** Yes — for every user (`login` → `add-to-cart` → `logout`), the exact order is preserved because Kafka guarantees ordering within a single partition.

---

## 👥 Part 3: Consumer Groups

### 1. Two Consumers Sharing `ironhack-group`
- Started two consumers in **Window A** and **Window B** with the same `--group ironhack-group`:
  ```bash
  docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group ironhack-group --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
  ```
- Sent 6 keyed messages from **Window C** (`user1:one` through `user6:six`). Each message appeared in **only one** of the two consumer windows.
- Described the group:
  ```bash
  docker exec -it kafka /opt/kafka/bin/kafka-consumer-groups.sh --describe --group ironhack-group --bootstrap-server localhost:9092
  ```
- **Verified Output (2 members splitting 3 partitions, `LAG = 0`):**
  ```text
  GROUP           TOPIC   PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG  CONSUMER-ID
  ironhack-group  orders  0          7               7               0    console-consumer-3c747b63-...
  ironhack-group  orders  1          4               4               0    console-consumer-3c747b63-...
  ironhack-group  orders  2          10              10              0    console-consumer-f21fb417-...
  ```
  - Consumer 1 owned **Partitions 0 & 1**; Consumer 2 owned **Partition 2**.

### 2. Automatic Failover (Stopping Window B)
- Pressed `Ctrl-C` in **Window B** and sent two more messages (`user1:after-failover`, `user2:after-failover`).
- **Verified:** Consumer 1 (`...3c747b63`) automatically rebalanced and took over **all 3 partitions (0, 1, 2)** with `LAG = 0` (`Partition 0: 7 → 8`, `Partition 2: 10 → 11`).

### 3. Second Independent Consumer Group (`other-group`)
```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group other-group --from-beginning --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```
- **Verified:** Because `other-group` tracks its own offsets independently, it received **all 23 messages** in `orders` from the very beginning (`Partition 0: 8`, `Partition 1: 4`, `Partition 2: 11`, `LAG = 0`).

---

## 💬 Part 4: Chat in Two Windows

- *(Already completed in the previous session / Lab 1 live chat demo, so skipped here as noted in the lab handout.)*

---

## 🧹 Clean Up

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --delete --topic orders --bootstrap-server localhost:9092
```
- **Verified:** Topic `orders` deleted cleanly.

---

## 📝 Review Questions & Answers

1. **What is a partition, and why does a topic have more than one?**  
   A partition is an ordered, append-only log that makes up part of a topic. Having multiple partitions lets Kafka store data across brokers and lets multiple consumers in a group read and process messages in parallel.

2. **Why is it useful that messages with the same key go to the same partition?**  
   Because Kafka guarantees message order **within a single partition**. Sending all events for the same key (like one user or one order) to the same partition guarantees they are always processed in the exact order they happened.

3. **A topic has 3 partitions and a group has 4 consumers. How many consumers sit idle?**  
   **1 consumer** sits idle, because each partition can only be read by **one** consumer in the same consumer group at a time (so 3 consumers get 1 partition each, and the 4th has no partition assigned).

4. **Two consumers with different group names read the same topic. What does each receive?**  
   Each consumer group receives **every message** in the topic independently, because Kafka tracks offsets separately for each consumer group.

5. **Does Kafka guarantee the order of messages across the whole topic?**  
   **No.** Kafka only guarantees strict ordering **within a single partition**, not across different partitions of the same topic.
