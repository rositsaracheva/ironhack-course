# LAB | Introduction to Hadoop and Distributed Storage

**Week 4 — Day 3: Introduction to Hadoop and Distributed Storage — Lab**  
---

## Practice Workbook Overview

BritMart stores large amounts of sales and application data. This lab focuses on:
- Why Hadoop was created (handling massive data that does not fit on one computer).
- How HDFS (Hadoop Distributed File System) breaks down and stores large files.
- How replication protects data when hardware fails.

---

## Part 1 — Why Hadoop and Distributed Storage

### Q. 1 — Scale Up or Scale Out?

**Question:** Complete the table.

| Change | Scale up or scale out? |
| :--- | :--- |
| Add more RAM to one server | **Scale up** |
| Add four worker machines | **Scale out** |
| Replace one CPU with a faster CPU | **Scale up** |
| Add three storage nodes | **Scale out** |

> **Notes to understand this:**
> - **Scale Up (Vertical Scaling):** Making **one** existing machine bigger or more powerful (e.g., adding more RAM, faster CPU, bigger hard drive).
> - **Scale Out (Horizontal Scaling):** Adding **more** machines to work together as a cluster (e.g., adding 4 worker servers or 3 storage nodes). Hadoop is built around scaling out!

---

### Q. 2 — Calculate HDFS Blocks

**Given:**
- File size = `700 MB`
- Block size = `128 MB`

**Calculation:**
1. Divide file size by block size:
   $$\frac{700\text{ MB}}{128\text{ MB}} = 5.46875$$
2. Since any remaining data needs its own full block, we round up to the next whole number.

**Breakdown of blocks:**
- Block 1: 128 MB
- Block 2: 128 MB
- Block 3: 128 MB
- Block 4: 128 MB
- Block 5: 128 MB  *(Total so far = 5 × 128 = 640 MB)*
- Block 6: 60 MB *(Remaining data: 700 - 640 = 60 MB)*

**Answer:**
**6 HDFS blocks** are needed.

---

### Q. 3 — Calculate Blocks with Python

**Given:**
- File size = `1,025 MB`
- Block size = `128 MB`

**Python Code:**

```python
import math

# Define file size and block size in MB
file_size = 1025
block_size = 128

# Use math.ceil() to always round up to the next integer
num_blocks = math.ceil(file_size / block_size)

print(f"Number of blocks needed: {num_blocks}")
```

**Output:**
```text
Number of blocks needed: 9
```

> **Why 9 blocks?**  
> $1025 / 128 = 8.0078$. Because there is a tiny fraction left over (just 1 MB), HDFS must allocate a 9th block for it.

---

### Q. 4 — MCQ: Scaling Out

**Question:** What does scaling out mean?
- A. Run every task on one server
- B. Increase RAM on one machine
- C. Replace one disk with a larger disk
- **D. Add more machines to share the work**

**Answer:** **D. Add more machines to share the work**

> **Explanation:** Scaling out means horizontal scaling — adding multiple commodity computers so they can share both the storage and the processing workload.

---

## Part 2 — NameNode, DataNodes, and File Reads

### Q. 5 — Classify HDFS Responsibilities

**Question:** Mark each item as mainly **NameNode** or **DataNode**.

- **A. Stores file-system metadata:** **NameNode**  
  *(The NameNode acts as the master directory; it keeps file names, permissions, and directory trees).*
- **B. Stores actual block contents:** **DataNode**  
  *(DataNodes are the workers; they save the actual bytes/blocks on their local hard drives).*
- **C. Tracks block locations:** **NameNode**  
  *(The NameNode remembers which DataNodes hold which blocks).*
- **D. Sends heartbeats:** **DataNode**  
  *(DataNodes regularly ping the NameNode to say "I am alive and healthy").*
- **E. Serves block data to clients:** **DataNode**  
  *(Clients read and write the real file data directly from/to the DataNodes).*

---

### Q. 6 — Trace an HDFS Read

**Question:** Put these steps in order:

**Correct Order:**
1. **Client asks NameNode for block locations**  
   *(The client tells the NameNode: "I want to read file X. Where are its blocks?")*
2. **NameNode returns block locations**  
   *(The NameNode replies with a list of DataNodes holding the blocks).*
3. **Client reads blocks from DataNodes**  
   *(The client connects directly to the DataNodes to download the block data).*
4. **Client combines the block data**  
   *(The client stitches the blocks back together in order to reconstruct the full file).*

---

### Q. 7 — Simulate Block Placement

**Given:**
- File blocks: `B1, B2, B3, B4`
- BritMart DataNodes: `DN1, DN2, DN3`

**Valid Distribution Example:**
- **DN1:** Stores `B1`, `B4`
- **DN2:** Stores `B2`
- **DN3:** Stores `B3`

**Why spreading data helps parallel processing:**
> When the blocks of a file are spread across multiple nodes, each machine can read and process its assigned block at the exact same time using its own CPU, RAM, and disk. Instead of one single machine doing all 4 blocks one after another, all three machines work in parallel, making data processing significantly faster.

---

### Q. 8 — MCQ: NameNode

**Question:** What does the NameNode mainly store?
- **A. File-system metadata and block-location information**
- B. Every customer record
- C. Every replicated block copy
- D. Dashboard data

**Answer:** **A. File-system metadata and block-location information**

> **Explanation:** The NameNode does NOT store the actual file content or customer records. It only holds the metadata (the map and index) in memory.

---

## Part 3 — Small Files and Data Locality

### Q. 9 — Compare Two File Layouts

**Given:** BritMart has the same 10 GB of data in two designs:
- **Design A:** 100 files
- **Design B:** 1,000,000 files

**Question:** Which design creates more HDFS metadata pressure and why?

**Answer:** **Design B** creates much more HDFS metadata pressure.

**Why:**
> In HDFS, the NameNode holds all file system metadata in its physical memory (RAM) for fast lookup. Every file, directory, and block creates a metadata entry (approximately 150 bytes in RAM).
> - In **Design A**, the NameNode only has to keep track of 100 files (very little RAM).
> - In **Design B**, the NameNode must store 1,000,000 individual file records in RAM, even though the total data size is the same 10 GB. This exhausts NameNode memory and slows down the cluster. This is known as the **Small Files Problem** in Hadoop.

---

### Q. 10 — Calculate Metadata Entries Conceptually

**Given:**
- **Layout A:** 10 files, each file uses 2 blocks
- **Layout B:** 1,000 files, each file uses 1 block

**Calculation:**
- **Layout A:**
  $$10\text{ files} \times 2\text{ blocks/file} = \mathbf{20}\text{ block entries}$$
- **Layout B:**
  $$1,000\text{ files} \times 1\text{ block/file} = \mathbf{1,000}\text{ block entries}$$

**Summary:**  
Layout A only requires tracking **20 block entries**, while Layout B requires tracking **1,000 block entries** (50 times more!).

---

### Q. 11 — Explain Data Locality

**Scenario:** A processing task needs block `B3`.
- **Option A:** Run the task on a machine that already stores `B3`.
- **Option B:** Run it on another machine and transfer `B3` across the network.

**Question:** Which option better represents data locality, and why?

**Answer:** **Option A** better represents data locality.

**Why:**
> **Data locality** means moving the computation (the program/code) close to where the data already lives, rather than transferring heavy data across the network.
> - Running the task directly on the machine containing `B3` (Option A) reads the block from the local disk at high speed and avoids clogging the network bandwidth.

---

### Q. 12 — MCQ: Small Files

**Question:** Why can millions of tiny files be inefficient in HDFS?
- A. Every tiny file automatically gets ten replicas
- B. DataNodes cannot store small files
- **C. Every file and block creates metadata and processing overhead**
- D. The block size becomes zero

**Answer:** **C. Every file and block creates metadata and processing overhead**

> **Explanation:** Each file requires an entry in the NameNode's RAM, and processing frameworks (like MapReduce) launch separate tasks for each small file, wasting computing resources.

---

## Part 4 — Replication, Failure, and Rack Awareness

### Q. 13 — Calculate Replicated Storage

**Given:**
- File size = `700 MB`
- Replication factor = `3`

**Calculation:**
$$\text{Total Stored} = \text{File size} \times \text{Replication factor}$$
$$\text{Total Stored} = 700\text{ MB} \times 3 = \mathbf{2,100\text{ MB}}\quad (\text{or } 2.1\text{ GB})$$

**Answer:** **2,100 MB** (or 2.1 GB) of total data is stored across all replicas.

---

### Q. 14 — Calculate Storage for Three Files

**Given:**
- `files_mb = [100, 250, 400]`
- `replication_factor = 3`

**Python Code:**

```python
# List of file sizes in MB
files_mb = [100, 250, 400]
replication_factor = 3

# Calculate original total size
original_total = sum(files_mb)

# Calculate replicated total size
replicated_total = original_total * replication_factor

print(f"Original total: {original_total} MB")
print(f"Replicated total: {replicated_total} MB")
```

**Output:**
```text
Original total: 750 MB
Replicated total: 2250 MB
```

---

### Q. 15 — Trace a DataNode Failure

**Question:** Put these events in order:

**Correct Order:**
1. **DataNode stops sending heartbeats**  
   *(The worker machine crashes, has a disk failure, or loses network connection).*
2. **NameNode marks DataNode unavailable**  
   *(After waiting for a specific timeout period without heartbeats, the NameNode declares the node dead).*
3. **NameNode identifies under-replicated blocks**  
   *(The NameNode checks its metadata and sees which blocks now have fewer than 3 copies).*
4. **Replacement replicas are created**  
   *(The NameNode instructs remaining healthy DataNodes to copy the missing blocks so the replication factor is restored to 3).*

---

### Q. 16 — MCQ: Rack Awareness

**Question:** Why place replicas across different racks?
- A. To make all blocks smaller
- **B. To keep data available during a rack-level failure**
- C. To remove the need for DataNodes
- D. To guarantee every query is faster

**Answer:** **B. To keep data available during a rack-level failure**

> **Explanation:** In a data center, all servers in the same rack share a power source and a top-of-rack network switch. If an entire rack loses power or its switch dies, having copies on a different rack ensures the data is still accessible.

---

## Optional Practice

### Q. 17 — Compare Two Replication Choices

**Given:** A 5 TB dataset can use:
- Replication factor 2
- Replication factor 3

**Calculation:**
- **Replication factor 2:**  
  $$5\text{ TB} \times 2 = \mathbf{10\text{ TB}}\text{ total storage needed}$$
- **Replication factor 3:**  
  $$5\text{ TB} \times 3 = \mathbf{15\text{ TB}}\text{ total storage needed}$$

**Trade-off Explanation:**
> - **Replication Factor 2:**
>   - *Pros:* Saves 5 TB of disk space (cheaper storage cost and less network traffic during writes).
>   - *Cons:* Lower fault tolerance. It can only tolerate **1 machine failure**. If 2 machines holding the copies fail at the same time, data is permanently lost.
>
> - **Replication Factor 3 (Default in Hadoop):**
>   - *Pros:* High reliability and availability. It can tolerate **2 simultaneous node failures** and supports rack awareness. It also allows multiple clients to read data replicas in parallel.
>   - *Cons:* Consumes 50% more disk space (15 TB vs 10 TB), which increases hardware storage costs.
