'''
Data Cleaning
5. Convert the Salary column to numeric (handle errors).
6. Count how many missing (NaN) values are in each column.
7. Drop rows where Salary is missing.
8. Fill missing College values with "Unknown".
'''

import os        
import pandas as pd  

file_path = os.path.join(os.path.dirname(__file__), "nba.csv") 
df = pd.read_csv(file_path) 

# 5. Convert the Salary column to numeric (handle errors)

df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce") # pd.to_numeric converts text/numbers into float. errors="coerce" turns any invalid/empty text into NaN (missing value)
print("--- 5. Salary column converted to numeric ---") # prints section header
print(df["Salary"].dtypes) # .dtypes checks the data type --->(float64 confirms it is now numeric) 

# Why float64? NaN was originally invented as a mathematical signal for decimals, so Python and NumPy implemented it as a float. Whenever a column has missing values, Pandas uses float64 so it can fit NaN into the data.

# 6. Count how many missing (NaN) values are in each column

# Note: Here the dtype is int64 --> Counts are whole numbers, so their type is int64 (integer).

print("\n--- 6. Missing values per column ---") 
# .isna() marks every cell as True (if missing) or False (if present); .sum() adds up the True values per column
print(df.isna().sum())

# 7. Drop rows where Salary is missing

# .dropna() removes rows with NaN; subset=["Salary"] tells pandas to ONLY drop if the Salary column is empty
df = df.dropna(subset=["Salary"])
print("\n--- 7. Shape after dropping missing Salary rows ---") # \n adds a blank line for visual spacing
print(df.shape) # .shape returns (rows, columns) to show how many rows remain after dropping missing salaries

# 8. Fill missing College values with "Unknown"

# .fillna("Unknown") replaces every NaN value in the College column with the text "Unknown"
df["College"] = df["College"].fillna("Unknown")
print("\n--- 8. Missing values in College after fillna ---") # \n adds a blank line for visual spacing
print(df["College"].isna().sum()) # checks missing values in College again (should now be 0)

print("\nFirst 5 rows of cleaned data:") 
# df[["..."]] with double brackets filters and displays only these 4 specific columns; .head() shows top 5 rows
print(df[["Name", "Team", "College", "Salary"]].head())

'''
--- 5. Salary column converted to numeric ---
float64

--- 6. Missing values per column ---
Name         1
Team         1
Number       1
Position     1
Age          1
Height       1
Weight       1
College     85
Salary      12
dtype: int64

--- 7. Shape after dropping missing Salary rows ---
(446, 9)

--- 8. Missing values in College after fillna ---
0

First 5 rows of cleaned data:
            Name            Team        College      Salary
0  Avery Bradley  Boston Celtics          Texas   7730337.0
1    Jae Crowder  Boston Celtics      Marquette   6796117.0
3    R.J. Hunter  Boston Celtics  Georgia State   1148640.0
4  Jonas Jerebko  Boston Celtics        Unknown   5000000.0
5   Amir Johnson  Boston Celtics        Unknown  12000000.0
'''