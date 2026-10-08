''' 
1. Load the dataset into a DataFrame called df. 
2. Display the first 5 rows. 
3. Check the number of rows and columns. 
4. List all column names. 
'''

import os # built-in module to handle computer file paths safely
import pandas as pd # data analysis library; "as pd" is the standard shorthand alias

# 1. Load the dataset into a DataFrame called df.

file_path = os.path.join(os.path.dirname(__file__), "nba.csv") #this line creates the full path to the csv file making sure the script can find it regardless of where it is run from(even if we move the project to a different os)
df = pd.read_csv(file_path) # This line of code loads the nba dataset from the csv file into a pandas dataframe called df. it reads the data from file_path. 

# 2. Display the first 5 rows. Note: df.head()->(default is 5 rows).

print("\n2. First 5 rows:")
print(df.head())

# 3. Check the number of rows and columns.

print("\n3. Number of rows and columns (rows, columns):") # \n creates a blank space between lines
print(df.shape) 

# 4. List all column names.

print("\n4. Column names:")
print(df.columns.tolist())

'''
2. First 5 rows:
            Name            Team  Number Position   Age Height  Weight            College     Salary
0  Avery Bradley  Boston Celtics     0.0       PG  25.0    6-2   180.0              Texas  7730337.0
1    Jae Crowder  Boston Celtics    99.0       SF  25.0    6-6   235.0          Marquette  6796117.0
2   John Holland  Boston Celtics    30.0       SG  27.0    6-5   205.0  Boston University        NaN
3    R.J. Hunter  Boston Celtics    28.0       SG  22.0    6-5   185.0      Georgia State  1148640.0
4  Jonas Jerebko  Boston Celtics     8.0       PF  29.0   6-10   231.0                NaN  5000000.0

3. Number of rows and columns (rows, columns):
(458, 9)

4. Column names:
['Name', 'Team', 'Number', 'Position', 'Age', 'Height', 'Weight', 'College', 'Salary']
'''