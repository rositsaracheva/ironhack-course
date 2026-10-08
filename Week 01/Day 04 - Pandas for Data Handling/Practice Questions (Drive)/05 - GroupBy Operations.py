'''
GroupBy Operations
15. Find the average salary per team.
16. Count number of players in each team.
17. Find the maximum salary in each team.
'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 15. Find the average salary per team
avg_salary_team = df.groupby("Team")["Salary"].mean()        # .groupby("Team") groups by team; ["Salary"] targets salary; .mean() computes average
print("--- 15. Average Salary per Team ---")
print(avg_salary_team.head(10))                              # .head(10) displays results for the first 10 teams

# 16. Count number of players in each team
player_count_team = df.groupby("Team")["Name"].count()       # .groupby("Team") groups by team; ["Name"].count() counts player names in each team
print("\n--- 16. Number of Players in each Team ---")
print(player_count_team.head(10))                            # displays player counts for the first 10 teams

# 17. Find the maximum salary in each team
max_salary_team = df.groupby("Team")["Salary"].max()         # .groupby("Team") groups by team; ["Salary"].max() finds highest salary in each team
print("\n--- 17. Maximum Salary in each Team ---")
print(max_salary_team.head(10))                              # displays maximum salary for the first 10 teams

'''
--- 15. Average Salary per Team ---
Team
Atlanta Hawks            4.860197e+06
Boston Celtics           4.181505e+06
Brooklyn Nets            3.501898e+06
Charlotte Hornets        5.222728e+06
Chicago Bulls            5.785559e+06
Cleveland Cavaliers      7.642049e+06
Dallas Mavericks         4.746582e+06
Denver Nuggets           4.294424e+06
Detroit Pistons          4.477884e+06
Golden State Warriors    5.924600e+06
Name: Salary, dtype: float64

--- 16. Number of Players in each Team ---
Team
Atlanta Hawks            15
Boston Celtics           15
Brooklyn Nets            15
Charlotte Hornets        15
Chicago Bulls            15
Cleveland Cavaliers      15
Dallas Mavericks         15
Denver Nuggets           15
Detroit Pistons          15
Golden State Warriors    15
Name: Name, dtype: int64

--- 17. Maximum Salary in each Team ---
Team
Atlanta Hawks            18671659.0
Boston Celtics           12000000.0
Brooklyn Nets            19689000.0
Charlotte Hornets        13500000.0
Chicago Bulls            20093064.0
Cleveland Cavaliers      22970500.0
Dallas Mavericks         16407500.0
Denver Nuggets           14000000.0
Detroit Pistons          16000000.0
Golden State Warriors    15501000.0
Name: Salary, dtype: float64
'''
