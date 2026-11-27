# Week 08 — Day 05: Apache NiFi Flow-Based Processing Definitions

Here are my study definitions for all the key **Apache NiFi** flow-based processing concepts, written in simple, everyday words so they are easy to remember and explain in class.

*(Note: `funnel` appeared twice in the class list, so there are **17 unique concepts** below, kept in the exact class order.)*

---

## ⚡ Quick 1-Sentence Cheat Sheet (For Fast Class Answers)

| # | Term | Simple 1-Sentence Definition |
| :--- | :--- | :--- |
| 1 | **Dataflow** | The complete automated pipeline on the NiFi canvas that moves, transforms, and routes data from start to finish. |
| 2 | **FlowFile** | A single packet of data moving through NiFi, made of **Content** (the actual data) + **Attributes** (metadata labels). |
| 3 | **Processor** | A worker block on the canvas that performs one specific task (read, transform, filter, or save data). |
| 4 | **Processor Group** *(Process Group)* | A folder-like container on the canvas that groups processors and connections together to keep big pipelines organized. |
| 5 | **Funnel** | A small connector that merges FlowFiles coming from **multiple connections** into **one single connection**. |
| 6 | **Attribute** | Key-value metadata labels attached to the outside of a FlowFile (like `filename`, `path`, `uuid`, `fileSize`). |
| 7 | **Content** | The actual raw data or file body inside a FlowFile (such as text, CSV rows, JSON, or an image). |
| 8 | **Queue** | The waiting line (inside a connection arrow) that holds FlowFiles safely until the next processor is ready for them. |
| 9 | **Data Provenance** | NiFi's built-in tracking history that records every single event, step, and change a FlowFile went through. |
| 10 | **Penalty** *(Penalization)* | A temporary "time-out" (e.g., `30 sec`) put on **one problematic FlowFile** while the processor keeps working on other files. |
| 11 | **Yield** | A short pause (e.g., `1 sec`) put on **the entire Processor** so it stops running temporarily and doesn't waste CPU when a target system is down or empty. |
| 12 | **CRON Jobs / Scheduling** | Rules that control **when** a processor runs—either on a simple timer (every `5 sec`) or at exact calendar/clock times via CRON (e.g., every day at `2:00 AM`). |
| 13 | **Relationship (`success` / `failure`)** | Named exit paths leaving a processor that route a FlowFile depending on whether the task worked (`success`) or had an error (`failure`). |
| 14 | **Retry / Terminate** | Checkboxes on a relationship that either **try the processor again** (`retry`) or **end and delete the FlowFile** because its job is done (`terminate`). |
| 15 | **Back Propagation** *(Back Pressure)* | When a full queue automatically tells the **upstream processor behind it to pause** sending more data so NiFi doesn't run out of memory—propagating backward up the flow. |
| 16 | **Input Port** | The "entry door" of a Processor Group that lets FlowFiles come **into** the group from the outside canvas. |
| 17 | **Output Port** | The "exit door" of a Processor Group that sends finished FlowFiles **out of** the group back to the outside canvas. |

---

## 📖 Detailed Definitions & Everyday Examples (In My Own Words)

### 1. Dataflow
- **What it means:** A **dataflow** is the whole end-to-end automated pipeline I build on the NiFi canvas to collect data from a source, process or clean it, and deliver it to a destination.
- **Simple example:** My pipeline `GetFile` → `ReplaceText` → `PutFile` that picks up a text file from an input folder, changes lowercase `"hello"` to `"HELLO"`, and saves the result in an output folder.

### 2. FlowFile
- **What it means:** A **FlowFile** is the basic unit (single item) of data traveling through NiFi. Every FlowFile has two parts:
  1. **Content** (the actual payload/data inside), and
  2. **Attributes** (key-value information describing that data).
- **Simple analogy:** Like a sealed envelope in the mail—the letter inside is the **content**, and the address/tracking sticker on the outside is the **attributes**.

### 3. Processor
- **What it means:** A **Processor** is the main building block in NiFi that actually *does the work*—reading data, changing content, adding attributes, routing data, or writing it to an external system.
- **Simple example:** `GetFile` (reads files), `ReplaceText` (edits text), `LogAttribute` (writes attributes to the log), and `PutFile` (saves files).

### 4. Processor Group *(Process Group)*
- **What it means:** A **Processor Group** (called **Process Group** in NiFi) is like a folder on the NiFi canvas that holds a whole sub-pipeline of processors, queues, and ports inside one neat box.
- **Why we use it:** Instead of having 50 messy processors all over one screen, I can group related steps into logical boxes (like *Ingestion*, *Cleaning*, *Output*, or *Exercise 1*, *Exercise 2*, *Exercise 3*) and double-click to step inside.

### 5. Funnel *(listed twice on the worksheet)*
- **What it means:** A **Funnel** combines FlowFiles coming from several different processors or connections and sends them out through **one single connection** to the next processor.
- **Simple analogy:** Like three highway lanes merging into one lane—for example, taking the `failure` arrows from 4 different processors and merging them into one Funnel that feeds a single `LogAttribute` error processor.

### 6. Attribute
- **What it means:** An **Attribute** is a piece of metadata (information *about* the data) stored as a simple `key = value` text pair on a FlowFile, without touching the actual file content.
- **Simple example:** Every FlowFile automatically gets core attributes like:
  - `filename`: `'greeting.txt'`
  - `path`: `'./'`
  - `uuid`: `'582b2dc5-a7bc-4dbe-8cd2-cc1321d97de1'`

### 7. Content
- **What it means:** **Content** is the actual raw data bytes carried inside the FlowFile (really stored in NiFi's Content Repository, while the FlowFile holds a pointer to it).
- **Simple example:** If a FlowFile represents `greeting.txt`, the **attribute** is the name `greeting.txt`, and the **content** is the text `"hello world! hello Apache NiFi!"` written inside it.

### 8. Queue
- **What it means:** Every connection arrow between two processors contains a **Queue**—a temporary waiting line where FlowFiles sit safely after leaving Processor A until Processor B is ready to process them.
- **Why it helps:** In NiFi, I can right-click any queue to **List Queue** (inspect the FlowFiles waiting inside) or **Empty Queue** (clear stuck test files).

### 9. Data Provenance
- **What it means:** **Data Provenance** is NiFi's complete audit trail and lineage log. It records every event that happens to every FlowFile (`CREATE`, `RECEIVE`, `CONTENT_MODIFIED`, `ATTRIBUTES_MODIFIED`, `ROUTE`, `SEND`, `DROP`).
- **Simple analogy:** Like a FedEx/DHL package tracking page—I can click **View Data Provenance** on any processor to see where a FlowFile came from, how it changed before and after, and even replay it if something broke.

### 10. Penalty *(Penalization)*
- **What it means:** When a single FlowFile causes an error (for example, one bad record or a locked file), NiFi puts a **Penalty** (default `30 sec`) on **just that one FlowFile**. During those 30 seconds, NiFi ignores that penalized FlowFile and **continues processing all the other FlowFiles** in the queue.
- **Simple analogy:** One customer at the supermarket forgot their wallet, so the cashier asks *just that one customer* to step aside for 30 seconds while keeping the line moving for everyone else.

### 11. Yield
- **What it means:** **Yield** pauses **the entire Processor** for a short time (default `1 sec`) so NiFi stops scheduling it temporarily. This happens when there is nothing to do or when an external system (like a database or API) is completely unreachable, saving CPU resources.
- **Simple analogy:** Unlike *Penalty* (which pauses **1 FlowFile**), *Yield* pauses **the whole worker station**—if the database server is down, trying the next 5,000 files right now will also fail, so the processor rests for 1 second before checking again.

### 12. CRON Jobs / Scheduling
- **What it means:** In a processor's **Scheduling** tab, I choose *when* and *how often* NiFi runs that processor:
  - **Timer Driven (default):** Runs repeatedly on an interval (e.g., `0 sec` = as fast as possible, or `10 sec` = once every 10 seconds).
  - **CRON Driven:** Uses a **CRON expression** (6 fields in NiFi: `Seconds Minutes Hours Day-of-Month Month Day-of-Week`) to run at exact wall-clock schedules.
- **Simple example:** Setting CRON schedule `0 0 2 * * ?` tells NiFi to run the processor every night at exactly **02:00:00 AM**.

### 13. Relationship — `success` / `failure`
- **What it means:** After a processor finishes working on a FlowFile, it must send the FlowFile down a named exit route called a **Relationship**:
  - **`success`:** The processor completed its job cleanly with no errors, so the FlowFile moves forward to the next step.
  - **`failure`:** Something went wrong (bad format, missing permission, network error), so the FlowFile is sent down a separate path for error handling or logging instead of crashing the pipeline.
- **Important NiFi rule:** A processor shows a yellow warning triangle and **cannot start** until *every* relationship is either connected to another component or handled via `retry` / `terminate`.

### 14. Retry / Terminate
- **What it means:** Checkboxes on a processor's **Relationships** tab that handle an unconnected relationship automatically:
  - **`retry`:** Sends the FlowFile right back to the same processor to try again a configured number of times (e.g., retry `failure` 3 times in case of a brief network glitch).
  - **`terminate` (Auto-terminate):** Tells NiFi *"we don't need this FlowFile anymore—safely drop/delete it here."* For example, on the final `PutFile` step, I check `terminate` on `success` because the file has already been saved to disk.

### 15. Back Propagation *(Back Pressure in NiFi)*
- **What it means:** In NiFi flow-based processing, **Back Pressure** protects the system when a fast processor sends data into a slower processor. Every queue has two safety limits (by default **`10,000` objects** or **`1 GB` of data**). Once a queue hits that limit, NiFi automatically **stops running the upstream processor** feeding that queue until space opens up. If earlier queues fill up too, that stop signal **propagates backward** all the way up the pipeline.
- **Simple analogy:** Like traffic lights on a highway ramp—when the tunnel ahead is full, the light behind it turns red so cars don't crash or overflow the road.

### 16. Input Port
- **What it means:** An **Input Port** is the entry point placed inside a **Processor Group** so that processors or groups *outside* on the parent canvas can send FlowFiles **into** that group.
- **Simple analogy:** The "Receiving Door" of a warehouse department.

### 17. Output Port
- **What it means:** An **Output Port** is the exit point placed inside a **Processor Group** so that once the processors inside finish their work, they can pass the FlowFiles **out** to the parent canvas (to connect to the next Processor Group or processor).
- **Simple analogy:** The "Shipping Door" of a warehouse department.

---

## 💡 4 Classic Teacher Comparisons (Easy to Remember!)

1. **Attribute vs. Content:**
   - **Attribute** = the *label on the outside* of the envelope (`filename`, `size`, `uuid`).
   - **Content** = the *actual data inside* the envelope (the text, CSV, or JSON payload).
2. **Penalty vs. Yield:**
   - **Penalty** = puts **one single bad FlowFile** in time-out so other FlowFiles can keep moving.
   - **Yield** = pauses **the whole Processor** briefly to save CPU when an external system is down.
3. **Retry vs. Terminate:**
   - **Retry** = try processing this FlowFile again (`X` times) before giving up.
   - **Terminate** = finish and delete the FlowFile here because its journey is complete (or we intentionally discard it).
4. **Input Port vs. Output Port:**
   - **Input Port** = brings FlowFiles **into** a Processor Group.
   - **Output Port** = sends FlowFiles **out of** a Processor Group.
