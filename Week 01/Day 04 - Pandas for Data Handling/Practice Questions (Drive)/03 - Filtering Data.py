'''
Filtering Data
9. Show all players from Boston Celtics.
10. Show players whose Age is greater than 30.
11. Filter players who play as PG (Point Guard).
12. Find players with Salary greater than 5,000,000.
'''



import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "nba.csv")
df = pd.read_csv(file_path)

# 9. Show all players from Boston Celtics
boston_players = df[df["Team"] == "Boston Celtics"]         # == checks exact match; df[...] keeps only rows where condition is True
print("--- 9. Players from Boston Celtics ---")
print(boston_players[["Name", "Team", "Position"]])         # double brackets [[...]] print only Name, Team, and Position columns

# 10. Show players whose Age is greater than 30
players_over_30 = df[df["Age"] > 30]                        # > 30 checks if Age is strictly above 30; df[...] filters matching rows
print("\n--- 10. Players whose Age is greater than 30 ---")
print(players_over_30[["Name", "Age", "Team"]].head())      # .head() displays the first 5 matching players

# 11. Filter players who play as PG (Point Guard)
pg_players = df[df["Position"] == "PG"]                     # filters rows where Position column equals "PG"
print("\n--- 11. Players who play as PG ---")
print(pg_players[["Name", "Position", "Team"]].head())      # displays the first 5 PG players

# 12. Find players with Salary greater than 5,000,000
high_earners = df[df["Salary"] > 5_000_000]                 # filters Salary > 5 million; underscores in 5_000_000 improve readability
print("\n--- 12. Players with Salary > 5,000,000 ---")
print(high_earners[["Name", "Team", "Salary"]].head())      # displays the first 5 players earning over 5M

'''
--- 9. Players from Boston Celtics ---
               Name            Team Position
0     Avery Bradley  Boston Celtics       PG
1       Jae Crowder  Boston Celtics       SF
2      John Holland  Boston Celtics       SG
3       R.J. Hunter  Boston Celtics       SG
4     Jonas Jerebko  Boston Celtics       PF
5      Amir Johnson  Boston Celtics       PF
6     Jordan Mickey  Boston Celtics       PF
7      Kelly Olynyk  Boston Celtics        C
8      Terry Rozier  Boston Celtics       PG
9      Marcus Smart  Boston Celtics       PG
10  Jared Sullinger  Boston Celtics        C
11    Isaiah Thomas  Boston Celtics       PG
12      Evan Turner  Boston Celtics       SG
13      James Young  Boston Celtics       SG
14     Tyler Zeller  Boston Celtics        C

--- 10. Players whose Age is greater than 30 ---
               Name   Age             Team
19     Jarrett Jack  32.0    Brooklyn Nets
31     Lou Amundson  33.0  New York Knicks
33  Carmelo Anthony  32.0  New York Knicks
34    Jose Calderon  34.0  New York Knicks
43    Sasha Vujacic  32.0  New York Knicks

--- 11. Players who play as PG ---
             Name Position            Team
0   Avery Bradley       PG  Boston Celtics
8    Terry Rozier       PG  Boston Celtics
9    Marcus Smart       PG  Boston Celtics
11  Isaiah Thomas       PG  Boston Celtics
19   Jarrett Jack       PG   Brooklyn Nets

--- 12. Players with Salary > 5,000,000 ---
             Name            Team      Salary
0   Avery Bradley  Boston Celtics   7730337.0
1     Jae Crowder  Boston Celtics   6796117.0
5    Amir Johnson  Boston Celtics  12000000.0
11  Isaiah Thomas  Boston Celtics   6912869.0
19   Jarrett Jack   Brooklyn Nets   6300000.0
'''
