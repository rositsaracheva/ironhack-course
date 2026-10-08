'''
Column Operations
21. Create a new column Age_in_5_years.
22. Create a new column Salary_in_Millions (Salary / 100000).
'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 21. Create a new column Age_in_5_years
df["Age_in_5_years"] = df["Age"] + 5                         # df["New_Col"] creates a new column; df["Age"] + 5 adds 5 to every player's age
print("--- 21. Age and Age_in_5_years ---")
print(df[["Name", "Age", "Age_in_5_years"]].head())          # selects and displays these 3 columns for the first 5 rows

# 22. Create a new column Salary_in_Millions (Salary / 100000)
df["Salary_in_Millions"] = df["Salary"] / 100000             # divides Salary by 100,000 (per question instructions) and stores in new column
print("\n--- 22. Salary and Salary_in_Millions ---")
print(df[["Name", "Salary", "Salary_in_Millions"]].head())   # displays original and new salary columns side by side for first 5 players

'''
--- 21. Age and Age_in_5_years ---
            Name   Age  Age_in_5_years
0  Avery Bradley  25.0            30.0
1    Jae Crowder  25.0            30.0
2   John Holland  27.0            32.0
3    R.J. Hunter  22.0            27.0
4  Jonas Jerebko  29.0            34.0

--- 22. Salary and Salary_in_Millions ---
            Name     Salary  Salary_in_Millions
0  Avery Bradley  7730337.0            77.30337
1    Jae Crowder  6796117.0            67.96117
2   John Holland        NaN                 NaN
3    R.J. Hunter  1148640.0            11.48640
4  Jonas Jerebko  5000000.0            50.00000
'''
