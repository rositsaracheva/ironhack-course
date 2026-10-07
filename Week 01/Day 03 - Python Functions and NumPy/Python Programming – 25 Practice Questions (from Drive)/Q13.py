# Question 13: for Loops
# Write a program to print all numbers between 1 and 100 that are divisible by both 3 and 5.

for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print(number)


'''

15
30
45
60
75
90

'''
