#OCTOBER 8 |  Day 4: Pandas for Data Handling

#
#
'''
import pandas as pd 

# From a list
ages = pd.Series([21, 19, 22, 20])
#print(ages)
# With custom index
ages = pd.Series([21, 19, 22, 20], index=["Alex", "Maria", "John", "Sara"])
print(ages)

# From a dictionary
data = {
    "name": ["Alex", "Maria", "John", "Sarah"],
    "age": [25, 19, 22, 20],
    "score": [85, 78, 23.5, 78]
}

#print(data)
df = pd.DataFrame(data)
print(df)
'''

# load a csv.file 

'''

import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "students.csv")
df = pd.read_csv(file_path, header=0)
print(df)

'''

'''

  id   name  age  score
0   1   Alex   21     85
1   2  Maria   19     78
2   3   John   22     90
3   4   Sara   20     88
4   5  David   18     72

'''


