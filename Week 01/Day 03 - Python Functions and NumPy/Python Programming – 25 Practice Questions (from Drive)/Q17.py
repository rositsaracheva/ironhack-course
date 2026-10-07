# Question 17: Lists + Loops
# Given the following list:
# numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]
# Use a for loop to print:
# - All even numbers
# - All odd numbers
# - All numbers greater than 50

numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]

print("--- Even numbers ---")
for num in numbers:
    if num % 2 == 0:
        print(num)

print("\n--- Odd numbers ---")
for num in numbers:
    if num % 2 != 0:
        print(num)

print("\n--- Numbers greater than 50 ---")
for num in numbers:
    if num > 50:
        print(num)


'''

--- Even numbers ---
12
56
34
10

--- Odd numbers ---
45
7
89
23
91

--- Numbers greater than 50 ---
89
56
91

'''
