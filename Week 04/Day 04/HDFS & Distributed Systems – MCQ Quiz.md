# HDFS & Distributed Systems – MCQ Quiz (Questions 1–13)

---

### 1. What does HDFS stand for?
- a) High Distribution File System
- **b) Hadoop Distributed File System**
- c) Hierarchical Data File System
- d) Hadoop Data Framework System

**Answer:** **b) Hadoop Distributed File System**

**Explanation:** HDFS is the storage part of the Apache Hadoop framework. "Distributed File System" means that instead of storing a huge file on just one computer (which might run out of space or crash), it splits the file into pieces and spreads ("distributes") them across many computers working together in a cluster.

---

### 2. In HDFS, what is the default block size in Hadoop 2.x and later?
- a) 64 MB
- b) 32 MB
- **c) 128 MB**
- d) 256 MB

**Answer:** **c) 128 MB**

**Explanation:** When you save a large file in HDFS, it chops the file into equal-sized chunks called **blocks**. In older versions of Hadoop (Hadoop 1.x), the default chunk size was 64 MB, but starting in Hadoop 2.x, it was increased to **128 MB**. Using large blocks (compared to normal computer hard drives, which use tiny 4 KB blocks) makes it much faster to read and manage massive files.

---

### 3. Which component of HDFS is responsible for storing metadata about files and blocks?
- a) DataNode
- **b) NameNode**
- c) Secondary NameNode (StandBy namenode) HA mode (High Availability)
- d) ResourceManager

**Answer:** **b) NameNode**

**Explanation:** A **NameNode** is as the "table of contents" or "librarian" of HDFS. It does not store the actual data inside your files. Instead, it stores **metadata**—information *about* your files, such as file names, permissions, how a file is split into blocks, and which DataNodes (worker computers) hold each block.

---

### 4. What is the default replication factor in HDFS?
- a) 1
- b) 2
- **c) 3**
- d) 5

**Answer:** **c) 3**

**Explanation:** Because computers can break or lose power at any time, HDFS automatically makes backup copies of every data block. By default, the **replication factor is 3**, meaning every single block of data is saved on **3 different computers (DataNodes)**. If one computer crashes, your data is still safe on the other two!

---

### 5. What is the primary role of the Secondary NameNode?
- a) Acts as a backup NameNode for failover
- **b) Periodically merges the FsImage and EditLogs**
- c) Stores actual data blocks
- d) Manages resource allocation

**Answer:** **b) Periodically merges the FsImage and EditLogs**

**Explanation:** Despite its confusing name, the **Secondary NameNode is NOT a backup** that takes over if the NameNode crashes. Instead, it is a helper assistant. The main NameNode keeps a snapshot of the file system (**FsImage**) and a diary of every recent change (**EditLogs**). Over time, that diary gets huge. The Secondary NameNode periodically takes the snapshot and the diary, merges them together into a fresh, clean snapshot (checkpointing), and sends it back to the NameNode so the NameNode doesn't get slowed down.

---

### 6. Which of the following best describes the CAP theorem?
- a) A system can guarantee Consistency, Availability, and Partition tolerance simultaneously
- **b) A distributed system can only guarantee at most two of Consistency, Availability, and Partition tolerance**
- c) A system must sacrifice Consistency for scalability
- d) CAP applies only to relational databases

**Answer:** **b) A distributed system can only guarantee at most two of Consistency, Availability, and Partition tolerance**

**Explanation:** The **CAP theorem** is a famous rule in distributed systems. It talks about three goals:
1. **Consistency (C):** Every computer shows the exact same, up-to-date data at the same time.
2. **Availability (A):** The system always responds to requests, even if some computers are down.
3. **Partition tolerance (P):** The system keeps working even if network cables break and computers can't talk to each other.

The theorem states you **cannot have all three at once**—when a network failure (Partition) happens, you must choose between giving the user an immediate answer that might be slightly outdated (**Availability**) or making the user wait/blocking the request until all computers agree on the exact latest data (**Consistency**).

---

### 7. In HDFS architecture, what is a "rack awareness" policy used for?
- a) Encrypting data across racks
- **b) Optimizing network bandwidth and improving fault tolerance by considering node placement**
- c) Balancing CPU load across nodes
- d) Managing user authentication

**Answer:** **b) Optimizing network bandwidth and improving fault tolerance by considering node placement**

**Explanation:** In a data center, servers (nodes) are stacked in physical cabinets called **racks**. All computers in the same rack share one power supply and network switch. If HDFS put all 3 copies of a block in the same rack and that rack lost power, you would lose your data! **Rack awareness** means the NameNode knows which physical rack each computer lives in. It places copies across *different* racks (for safety/fault tolerance) while keeping two copies in the same rack (to save network bandwidth and speed up transfers).

---

### 8. Which protocol does HDFS primarily use for communication between client and NameNode?
- a) FTP
- b) HTTP only
- **c) RPC (Remote Procedure Call) (SSH)**
- d) SMTP

**Answer:** **c) RPC (Remote Procedure Call)** **--> **(SSH) is a different thing, shouldn´t be here?**

**Explanation:** **RPC (Remote Procedure Call)** is a communication protocol that lets one program (like your HDFS client or a DataNode) ask another program on a different computer (the NameNode) to run a function and return the result—almost as if it were a local function call. HDFS uses RPC over TCP/IP for fast, lightweight communication between clients, DataNodes, and the NameNode.

---

### 9. What happens when a DataNode fails in HDFS?
- a) The entire cluster stops
- **b) The NameNode detects it via missed heartbeats and re-replicates blocks to other DataNodes**
- c) Data is permanently lost
- d) The Secondary NameNode takes over as DataNode

**Answer:** **b) The NameNode detects it via missed heartbeats and re-replicates blocks to other DataNodes**

**Explanation:** Every DataNode sends a regular "I'm alive!" signal (called a **heartbeat**) to the NameNode every few seconds. If a DataNode crashes and stops sending heartbeats, the NameNode marks it as dead. Since the blocks that were on that crashed computer now only have 2 copies left instead of 3, the NameNode automatically tells the surviving DataNodes to make new copies onto healthy computers so the replication factor goes back up to 3.

---

### 10. In distributed systems, what is "eventual consistency"?
- a) All nodes are always consistent immediately
- **b) Given enough time without new updates, all replicas will converge to the same value**
- c) Consistency is never achieved
- d) Only the primary node needs to be consistent

**Answer:** **b) Given enough time without new updates, all replicas will converge to the same value**

**Explanation:** When you update data in a big distributed system (like posting a photo or updating a status), copying that change to servers all around the world takes a tiny bit of time. **Eventual consistency** means that for a brief moment, Server A might have the new value while Server B still has the old value—but once you stop making new changes, all copies will catch up ("converge") and eventually become identical everywhere.

---

### 11. What is the purpose of the "heartbeat" mechanism in HDFS?
- a) To encrypt data transfers
- **b) To signal that a DataNode is alive and functioning to the NameNode**
- c) To balance load between clients
- d) To trigger block replication manually

**Answer:** **b) To signal that a DataNode is alive and functioning to the NameNode**

**Explanation:** Just like a doctor checks a patient's pulse to know they are alive, the NameNode listens for a **heartbeat** signal from every DataNode (by default, every 3 seconds). If the NameNode doesn't hear a heartbeat from a DataNode for a set period (usually 10 minutes), it assumes that DataNode has crashed and stops sending users to it.

---

### 12. Which of the following is a single point of failure in classic (non-HA) HDFS architecture?
- a) DataNode
- **b) NameNode**
- c) Secondary NameNode
- d) Client

**Answer:** **b) NameNode**

**Explanation:** A **Single Point of Failure (SPOF)** is a component that, if it breaks, brings down the entire system. In classic Hadoop (Hadoop 1.x, before High Availability mode was invented), there was only **one NameNode**. Even if all your DataNodes were healthy and holding your files, if the single NameNode crashed, nobody could look up where any blocks were stored—making the whole HDFS cluster unusable until the NameNode was fixed.

---

### 13. What is "write-once-read-many" (WORM) in the context of HDFS?
- a) A security protocol
- **b) A file access model where files are written once and read multiple times without modification**
- c) A backup strategy
- d) A replication algorithm

**Answer:** **b) A file access model where files are written once and read multiple times without modification**

**Explanation:** HDFS was designed around the idea that once you upload a big dataset (write it once), you won't go back and edit words in the middle of the file. Instead, you will run many analytics jobs and queries on that file over and over again (**read many times**). Because HDFS doesn't have to worry about multiple people editing the middle of a file at the same time, it can be much simpler and faster at streaming huge amounts of data.

---

### *Bonus (Unnumbered question right below #13 on the quiz sheet): In distributed systems, what does "sharding" refer to?
- a) Encrypting data across nodes
- **b) Partitioning data across multiple servers/nodes to distribute load**
- c) Replicating entire datasets on every node
- d) Compressing data before storage

**Answer:** **b) Partitioning data across multiple servers/nodes to distribute load**

**Explanation:** **Sharding** means taking a giant database or dataset and splitting it horizontally into smaller pieces (called "shards"), then storing each piece on a different server. For example, Server 1 stores customers A–M, and Server 2 stores customers N–Z. This spreads out the storage and workload so no single computer gets overwhelmed.

