# dbt Installation & Quickstart Guide for macOS

## Installing and Running dbt on macOS with VS Code and DuckDB

This guide explains how to install **dbt Core** on **macOS** using VS Code and **DuckDB**, then create and run a simple business demo using a CSV seed file and SQL transformations.

---

### Step 1 — Check Python Installation
Open Terminal (`Applications > Utilities > Terminal` or inside VS Code) and verify your Python version:

```bash
python3 --version
```

If Python is not installed, install it via [Homebrew](https://brew.sh) or download it from [python.org](https://www.python.org/downloads/macos/):
```bash
brew install python
```

---

### Step 2 — Install VS Code
Download and install Visual Studio Code:
[https://code.visualstudio.com](https://code.visualstudio.com)

**Recommended Extensions:**
- **Python** (by Microsoft)
- **dbt Power User** (optional, recommended for dbt development)
- **SQLTools / SQLite / DuckDB** (optional)

---

### Step 3 — Create Project Folder
Open your terminal and create the directory where your work will live:

```bash
mkdir -p "dbt_demo"
cd "dbt_demo"
```

Open this folder in VS Code:
```bash
code .
```
*(Or use `File > Open Folder...` in VS Code)*

---

### Step 4 — Open Terminal in VS Code
Inside VS Code:
- Go to the menu: `Terminal` → `New Terminal`
- Verify that the terminal shell is **zsh** or **bash** (default on macOS).

---

### Step 5 — Create Virtual Environment
Create an isolated Python environment named `dbt_env`:

```bash
python3 -m venv dbt_env
```

---

### Step 6 — Activate Environment
Activate the virtual environment on macOS:

```bash
source dbt_env/bin/activate
```

Successful activation displays the environment prefix:
```text
(dbt_env) user@MacBook dbt_demo %
```

---

### Step 7 — Upgrade pip
Ensure your package manager is up to date:

```bash
python3 -m pip install --upgrade pip
```

---

### Step 8 — Install dbt with DuckDB Adapter
Install `dbt-duckdb` (which automatically installs `dbt-core` and the DuckDB engine):

```bash
pip install dbt-duckdb
```

---

### Step 9 — Verify Installation
Check that dbt is correctly installed:

```bash
dbt --version
```

Expected output includes:
- `Core: installed: 1.x.x`
- `Plugins: duckdb: 1.x.x`

---

### Step 10 — Initialize dbt Project
Initialize a new project called `my_first_project`:

```bash
dbt init my_first_project
```

When prompted:
```text
Which database would you like to use?
[1] duckdb
Enter a number: 1
```

---

### Step 11 — Move Into Project Directory
Always run dbt commands from inside the root of your dbt project:

```bash
cd my_first_project
```

---

### Step 12 — Create CSV File (Seed Data)
Inside the `seeds/` folder, create a file named `sales_data.csv`:

```bash
# Path: seeds/sales_data.csv
```

Paste the following data into `sales_data.csv`:
```csv
order_id,customer,product,amount
1001,Alice,Laptop,75000
1002,Bob,Mouse,1200
1003,Alice,Keyboard,2500
1004,Charlie,Monitor,15000
1005,Bob,Phone,65000
```

---

### Step 13 — Load CSV into DuckDB
Load the CSV file into your local DuckDB database:

```bash
dbt seed
```

**Expected message:**
```text
1 of 1 OK loaded seed file main.sales_data [INSERT 5 in 0.04s]
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```

---

### Step 14 — Create dbt Model
Inside `models/example/`, create a new SQL file named `customer_sales.sql`:

```bash
# Path: models/example/customer_sales.sql
```

Paste the transformation query:
```sql
SELECT
    customer,
    SUM(amount) AS total_sales
FROM {{ ref('sales_data') }}
GROUP BY customer
```

*(Optional: document your model by adding its entry to `models/example/schema.yml`)*

---

### Step 15 — Run the Model
Execute the transformation to create the view/table in DuckDB:

```bash
dbt run
```

**Expected message:**
```text
1 of 3 OK created sql view model main.customer_sales
Completed successfully. PASS=3
```

---

### Step 16 — View Result in Terminal
Preview the calculated model directly from your terminal:

```bash
dbt show --select customer_sales
```

**Expected output:**
```text
| customer | total_sales |
| -------- | ----------- |
| Bob      |       66200 |
| Charlie  |       15000 |
| Alice    |       77500 |
```

---

### Step 17 — Generate and View Documentation
Generate the interactive catalog and lineage graph:

```bash
dbt docs generate
dbt docs serve
```

A web browser tab will automatically open at `http://localhost:8080`, showing your models, columns, descriptions, and the dependency lineage graph (DAG).  
*(To stop the server in terminal, press `Ctrl + C`)*

---

## Key Differences: macOS vs Windows

| Action | Windows (Original Guide) | macOS (Adapted) |
| :--- | :--- | :--- |
| **Python command** | `python` | `python3` |
| **Terminal shell** | Command Prompt (`cmd.exe`) | Zsh / Bash |
| **Virtualenv activation** | `dbt_env\Scripts\activate` | `source dbt_env/bin/activate` |
| **File path separators** | Backslashes (`\`) | Forward slashes (`/`) |
| **Profiles directory** | `C:\Users\<user>\.dbt` | `~/.dbt/` (`/Users/<user>/.dbt`) |

---

## Common Beginner Errors & Fixes (macOS)

- **`zsh: command not found: dbt`**:
  Your virtual environment is not active. Run:
  ```bash
  source dbt_env/bin/activate
  ```
- **`The directory [...] does not appear to be a dbt project`**:
  Make sure you ran `cd my_first_project`. All `dbt run`, `dbt seed`, and `dbt show` commands must be executed from inside the project folder where `dbt_project.yml` is located.
- **Ensure CSV file is inside the `seeds/` folder** and has a `.csv` extension (not `.xlsx` or `.txt`).
- **Always save SQL files in VS Code (`Cmd + S`)** before running `dbt run`.

---

## Final Pipeline Flow

```text
sales.csv  ──▶  dbt seed  ──▶  stg_sales (cleaning & tests)  ──▶  customer_sales  ──▶  analytics
```

---

## Part 2: Data Cleaning & Automated Quality Tests (stg_sales)

### Step 18 — Create Staging Model (`stg_sales.sql`)
Inside `models/example/`, create [`stg_sales.sql`](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2004/Day%2001/dbt_demo/my_first_project/models/example/stg_sales.sql):

```sql
SELECT
    CAST(order_id AS INTEGER) AS order_id,
    TRIM(customer) AS customer_name,
    TRIM(product) AS product_name,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(price AS DECIMAL(12, 2)) AS unit_price,
    CAST(quantity AS DECIMAL(12, 2))
        * CAST(price AS DECIMAL(12, 2)) AS sales_amount
FROM {{ ref('sales') }}
WHERE quantity IS NOT NULL
    AND price IS NOT NULL
    AND quantity > 0
    AND price >= 0
```

### Step 19 — Configure Schema & Data Tests
In `models/example/schema.yml`, add test assertions (`unique`, `not_null`):

```yaml
version: 2

models:
  - name: stg_sales
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: customer_name
        data_tests:
          - not_null
      - name: quantity
        data_tests:
          - not_null
      - name: unit_price
        data_tests:
          - not_null
      - name: sales_amount
        data_tests:
          - not_null
```

### Step 20 — Seed, Run, and Test
Run the full testing cycle:

```bash
# 1. Seed raw data
dbt seed

# 2. Build models
dbt run

# 3. Execute quality tests
dbt test

# 4. Preview staging data
dbt show --select stg_sales

# 5. Update and serve docs
dbt docs generate
dbt docs serve
```

