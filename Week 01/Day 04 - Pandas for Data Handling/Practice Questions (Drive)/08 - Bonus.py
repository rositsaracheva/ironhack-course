'''
Bonus
23. Which team has the highest total salary payout?
24. Which position has the highest average salary?
'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 23. Which team has the highest total salary payout?
team_total_salary = df.groupby("Team")["Salary"].sum()       # groups players by team; ["Salary"].sum() calculates total payroll per team
highest_salary_team = team_total_salary.idxmax()             # .idxmax() returns the index label (Team name) with the highest total
highest_payout = team_total_salary.max()                     # .max() returns the highest numerical dollar amount

print("--- 23. Team with highest total salary payout ---")
print(f"{highest_salary_team}: ${highest_payout:,.2f}")      # f-string formats team and payout with commas and 2 decimals (:,.2f)

# 24. Which position has the highest average salary?
position_avg_salary = df.groupby("Position")["Salary"].mean() # groups by position; ["Salary"].mean() computes average salary per position
highest_avg_position = position_avg_salary.idxmax()          # .idxmax() returns the position abbreviation (e.g. C) with the highest average
highest_avg_salary = position_avg_salary.max()               # .max() returns the highest average numerical salary

print("\n--- 24. Position with highest average salary ---")
print(f"{highest_avg_position}: ${highest_avg_salary:,.2f}") # displays winning position with formatted salary
print("\nAll positions average salary:")
print(position_avg_salary.sort_values(ascending=False))      # .sort_values(ascending=False) displays all positions ranked from highest to lowest

'''
--- 23. Team with highest total salary payout ---
Cleveland Cavaliers: $106,988,689.00

--- 24. Position with highest average salary ---
C: $5,967,052.00

All positions average salary:
Position
C     5.967052e+06
PG    5.077829e+06
SF    4.857393e+06
PF    4.562483e+06
SG    4.009861e+06
Name: Salary, dtype: float64
'''
