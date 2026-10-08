#OCTOBER 8 |  ---- Day 4: Pandas for Data Handling ----

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
# I want all the people whose age is greater >=20 . Print only name and age
'''
import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "students.csv")
df = pd.read_csv(file_path, header=0)

print(df.loc[df["age"] >= 20, ["name", "age"]])

   name  age
0  Alex   21
2  John   22
3  Sara   20


'''
'''
import os
import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "students.csv")
df = pd.read_csv(file_path, header=0)

# Get John, Sara, David
print(df.iloc[2:5])

   id   name  age  score
2   3   John   22     90
3   4   Sara   20     88
4   5  David   18     72


'''
'''
import pandas as pd
data = {
    "Name": ["Alex", "Riya", "John", "Tony", "Sam"],
    "Department": ["HR", "IT", "IT", "HR", "IT"],
    "Salary": [30000, 50000, 45000, 32000, 52000]
}
df = pd.DataFrame(data)
print(df)
'''
'''
Name Department  Salary
0  Alex         HR   30000
1  Riya         IT   50000
2  John         IT   45000
3  Tony         HR   32000
4   Sam         IT   52000
'''

# --- Group By Examples ---
'''
# 1. Average salary per department
avg_salary = df.groupby("Department")["Salary"].mean()
print("\nAverage Salary per Department:")
print(avg_salary)

# 2. Total salary spend per department
total_salary = df.groupby("Department")["Salary"].sum()
print("\nTotal Salary per Department:")
print(total_salary)

# 3. Count employees in each department
employee_count = df.groupby("Department")["Name"].count()
print("\nNumber of Employees per Department:")
print(employee_count)

# 4. Multiple aggregations at once (mean, min, max)
salary_summary = df.groupby("Department")["Salary"].agg(["mean", "min", "max"])
print("\nSalary Summary per Department:")
print(salary_summary)

'''


