# Question 23: Functions
# Write a function calculate_sum(n) that uses a loop to calculate
# and return the sum of numbers from 1 to n.

def calculate_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

# Test the function:
user_n = int(input("Enter a number (n): "))
result = calculate_sum(user_n)
print(f"The sum of numbers from 1 to {user_n} is: {result}")


'''

Enter a number (n): 10
The sum of numbers from 1 to 10 is: 55

'''
