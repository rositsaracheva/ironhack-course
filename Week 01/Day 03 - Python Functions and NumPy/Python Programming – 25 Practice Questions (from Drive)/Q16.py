# Question 16: for Loops
# Write a program to count how many even numbers exist between 1 and 100.

count = 0

for number in range(1, 101):
    if number % 2 == 0:
        count += 1

print(f"There are {count} even numbers between 1 and 100.")


'''

There are 50 even numbers between 1 and 100.

'''
