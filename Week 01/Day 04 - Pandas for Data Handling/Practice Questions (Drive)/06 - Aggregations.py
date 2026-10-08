'''
Aggregations
18. What is the average age of players?
19. What is the maximum salary in the dataset?
20. What is the minimum weight?
'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 18. What is the average age of players?
avg_age = df["Age"].mean()                                   # .mean() calculates the mathematical average of all values in Age
print(f"--- 18. Average Age of players: {avg_age:.2f} ---")  # f-string embeds avg_age; :.2f rounds the number to 2 decimal places

# 19. What is the maximum salary in the dataset?
max_salary = df["Salary"].max()                              # .max() finds the single highest value in the Salary column
print(f"--- 19. Maximum Salary in the dataset: ${max_salary:,.2f} ---") # {:,.2f} formats with comma separators and 2 decimal places

# 20. What is the minimum weight?
min_weight = df["Weight"].min()                              # .min() finds the lowest weight in the Weight column
print(f"--- 20. Minimum Weight: {min_weight} lbs ---")       # f-string inserts min_weight followed by "lbs"

'''
--- 18. Average Age of players: 26.94 ---
--- 19. Maximum Salary in the dataset: $25,000,000.00 ---
--- 20. Minimum Weight: 161.0 lbs ---
'''
