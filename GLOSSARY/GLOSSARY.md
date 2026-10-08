# 📖 Python & Pandas Glossary & Symbol Dictionary


## 🔣 1. Symbols & Special Syntax

| Symbol / Syntax | Name | What it means & How to read it | Example |
| :--- | :--- | :--- | :--- |
| `\n` | **Newline Escape Character** | Inserts a blank line (acts like pressing the `Enter` key). Used inside strings for visual spacing. | `print("\nFirst 5 rows:")` |
| `#` | **Comment** | Everything after `#` on that line is ignored by Python. Used to write notes and explanations. | `df.shape # returns (rows, cols)` |
| `'''` or `"""` | **Triple Quotes (Docstring)** | Allows text to span multiple lines. Used for multi-line notes, questions, or terminal outputs. | `'''\nQuestion 1\n'''` |
| `5_000_000` | **Underscore in numbers** | Visual thousands separator. Python treats `5_000_000` exactly the same as `5000000`, but it is easier for humans to read. | `df["Salary"] > 5_000_000` |
| `f"..."` | **f-String (Formatted String)** | Allows you to plug variables directly into text inside `{curly_brackets}` without messy concatenation. | `f"Average: {avg_age}"` |
| `{val:.2f}` | **Decimal Formatting** | Rounds a float number to **2 decimal places**. `.2` = 2 digits, `f` = float. | `f"{avg_age:.2f}"` (e.g. `26.94`) |
| `{val:,.2f}` | **Currency / Number Formatting** | Formats numbers with **commas for thousands** and **2 decimals**. | `f"${max_salary:,.2f}"` (e.g. `$25,000,000.00`) |
| `=` | **Assignment Operator** | Stores the result on the right into the variable on the left. | `df = pd.read_csv(...)` |
| `==` | **Equality Comparison** | Compares two values: returns `True` if equal, `False` if not. | `df["Team"] == "Boston Celtics"` |
| `>`, `<` | **Comparison Operators** | Strictly greater than (`>`), strictly less than (`<`). | `df["Age"] > 30` |
| `df["Column"]` | **Single Bracket** | Selects a **single column** as a Pandas Series (1-dimensional list of values). | `df["Age"]` |
| `df[["Col1", "Col2"]]`| **Double Brackets** | Selects **multiple columns** as a DataFrame (2-dimensional sub-table). | `df[["Name", "Salary"]]` |
| `df[ condition ]` | **Boolean Filter** | Keeps only the rows where the inside condition evaluates to `True`. | `df[df["Position"] == "PG"]` |
| `()` | **Parentheses (Call)** | Executes/calls a function or method. | `df.head()`, `df.mean()` |

| ''' df.mean = calculates the average value of your data (it adds all the numbers together and divides by the total count).
--- 1. On a Single Column (Most Common)
| You specify which column you want to average:
df["Age"].mean() --> What it does: Adds up all the players' ages and divides by the number of players.

| 2. On the Entire  --> df.mean(numeric_only=True)--> What it does: Calculates the average for every numeric column at once (e.g. average Number, average Age, average Weight, average Salary).'''


---

## 📁 2. File & Path Utilities (`os`)

| Code | Explanation |
| :--- | :--- |
| `import os` | Imports Python's built-in Operating System module to handle files and folder paths safely across macOS, Windows, and Linux. |
| `__file__` | A special Python variable that represents the exact path of the script currently running. |
| `os.path.dirname(__file__)` | Extracts the folder/directory where this script is located. |
| `os.path.join(folder, "nba.csv")` | Glues folder path and file name together using the correct system slash (`/` on Mac, `\` on Windows). Prevents `FileNotFoundError`. |

---

## 🐼 3. Core Pandas Concepts & Data Structures

| Term | What it is |
| :--- | :--- |
| **`import pandas as pd`** | Imports the Pandas data analysis library and gives it the industry-standard short nickname `pd`. |
| **`DataFrame` (`df`)** | A 2-dimensional table of rows and columns (just like an Excel spreadsheet or SQL table). |
| **`Series`** | A 1-dimensional column of data with an index. A DataFrame is made up of multiple Series side by side. |
| **`NaN`** | Stands for **"Not a Number"**. It is Pandas' standard representation for empty, missing, or null data. |

---

## 🔍 4. DataFrame Attributes (Inspect without `()`)

*Note: Attributes describe the structure of the table; they do NOT use parentheses `()`.*

| Attribute | What it does | Example Output |
| :--- | :--- | :--- |
| **`df.shape`** | Returns a tuple `(total_rows, total_columns)`. | `(458, 9)` |
| **`df.columns`** | Returns the list/index of all column header names. | `['Name', 'Team', 'Salary', ...]` |
| **`df.dtypes`** | Returns the data type of every column (`int64`, `float64`, `object`). | `Salary: float64` |

---

## ⚙️ 5. Essential Pandas Methods (With `()`)

| Method | What it does | Key Parameters / Options |
| :--- | :--- | :--- |
| **`pd.read_csv("path")`** | Reads a comma-separated values file and converts it into a DataFrame. | `header=0` (first row as headers) |
| **`df.head(n=5)`** | Returns the first `n` rows of the table (default is 5). | `df.head(10)` shows first 10 rows. |
| **`df.tail(n=5)`** | Returns the last `n` rows of the table. | `df.tail()` |
| **`pd.to_numeric(col)`** | Converts text data into numeric format (integers or decimals). | `errors="coerce"`: turns unconvertible/blank values into `NaN` instead of crashing. |
| **`df.isna()` / `df.isnull()`** | Checks every cell: returns `True` if empty (`NaN`), `False` if filled. | Often paired with `.sum()`. |
| **`df.isna().sum()`** | Sums up the `True` values column by column to show total missing values. | Output shows missing count per column. |
| **`df.dropna()`** | Removes rows that contain missing (`NaN`) values. | `subset=["Salary"]`: only checks and drops if `Salary` is missing. |
| **`df["Col"].fillna(val)`** | Replaces all missing (`NaN`) values in that column with a substitute value. | `df["College"].fillna("Unknown")` |
| **`df.sort_values(by=...)`** | Sorts table rows based on values in a column. | `ascending=False`: largest first (descending).<br>`ascending=True`: smallest first (ascending). |
| **`df.columns.tolist()`** | Converts the column headers index into a standard Python list. | `['Name', 'Age', 'Team']` |

---

## 👥 6. GroupBy & Aggregations

### The GroupBy Formula:
$$\text{df}.\text{groupby}(\text{"GroupColumn"})[\text{"ValueColumn"}].\text{aggregation}()$$

| Code | Explanation |
| :--- | :--- |
| **`df.groupby("Team")`** | Splits the table into separate subsets based on each unique team name. |
| **`df.groupby("Team")["Salary"].mean()`** | Groups by team, selects the Salary column, and calculates the **average salary** for each team. |
| **`df.groupby("Team")["Name"].count()`** | Groups by team and counts how many players belong to each team. |
| **`df.groupby("Team")["Salary"].max()`** | Groups by team and finds the highest salary paid on each team. |
| **`df.groupby("Team")["Salary"].sum()`** | Groups by team and calculates the total team payroll. |

### Overall Aggregations (Whole Dataset):
| Function | What it calculates | Example |
| :--- | :--- | :--- |
| **`.mean()`** | Mathematical average | `df["Age"].mean()` |
| **`.max()`** | Highest value | `df["Salary"].max()` |
| **`.min()`** | Lowest value | `df["Weight"].min()` |
| **`.sum()`** | Total sum | `df["Salary"].sum()` |
| **`.count()`** | Number of non-empty entries | `df["Name"].count()` |

---

## 🏆 7. Identifying Winners: `.max()` vs `.idxmax()`

| Function | What it returns | Example |
| :--- | :--- | :--- |
| **`series.max()`** | The highest **number/value** | `$106,988,689.00` |
| **`series.idxmax()`** | The **index label / name** that owns that highest value | `'Cleveland Cavaliers'` |

---

## ➕ 8. Creating New Columns

To add a new calculated column to your table:
```python
df["New_Column_Name"] = df["Existing_Column"] <math_operation>
```
- **Example 1:** `df["Age_in_5_years"] = df["Age"] + 5` (adds 5 to every age).
- **Example 2:** `df["Salary_in_Millions"] = df["Salary"] / 100000` (scales salaries down).
