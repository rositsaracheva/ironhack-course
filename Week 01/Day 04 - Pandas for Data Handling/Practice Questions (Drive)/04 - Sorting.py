'''
Sorting
13. Sort players by Salary (highest first).
14. Sort players by Age (youngest first).
'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 13. Sort players by Salary (highest first)
sorted_salary = df.sort_values(by="Salary", ascending=False) # .sort_values() orders rows; by="Salary" is the column; ascending=False sorts descending (highest first)
print("--- 13. Players sorted by Salary (highest first) ---")
print(sorted_salary[["Name", "Team", "Salary"]].head(10))    # .head(10) displays the top 10 rows instead of default 5

# 14. Sort players by Age (youngest first)
sorted_age = df.sort_values(by="Age", ascending=True)        # ascending=True sorts in ascending order (smallest to largest, so youngest first)
print("\n--- 14. Players sorted by Age (youngest first) ---")
print(sorted_age[["Name", "Age", "Team"]].head(10))          # displays the 10 youngest players with Name, Age, and Team

'''
--- 13. Players sorted by Salary (highest first) ---
                  Name                   Team      Salary
109        Kobe Bryant     Los Angeles Lakers  25000000.0
169       LeBron James    Cleveland Cavaliers  22970500.0
33     Carmelo Anthony        New York Knicks  22875000.0
251      Dwight Howard        Houston Rockets  22359364.0
339         Chris Bosh             Miami Heat  22192730.0
100         Chris Paul   Los Angeles Clippers  21468695.0
414       Kevin Durant  Oklahoma City Thunder  20158622.0
164       Derrick Rose          Chicago Bulls  20093064.0
349        Dwyane Wade             Miami Heat  20000000.0
294  LaMarcus Aldridge      San Antonio Spurs  19689000.0

--- 14. Players sorted by Age (youngest first) ---
                   Name   Age                    Team
226       Rashad Vaughn  19.0         Milwaukee Bucks
122        Devin Booker  19.0            Phoenix Suns
40   Kristaps Porzingis  20.0         New York Knicks
401          Tyus Jones  20.0  Minnesota Timberwolves
427     Cliff Alexander  20.0  Portland Trail Blazers
116    D'Angelo Russell  20.0      Los Angeles Lakers
441         Noah Vonleh  20.0  Portland Trail Blazers
356        Aaron Gordon  20.0           Orlando Magic
56        Jahlil Okafor  20.0      Philadelphia 76ers
445          Dante Exum  20.0               Utah Jazz
'''
