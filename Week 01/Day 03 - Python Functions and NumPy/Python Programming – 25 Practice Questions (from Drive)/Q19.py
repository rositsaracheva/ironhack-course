# Question 19: Lists + Loops
# Given a list of numbers, find the largest number without using the built-in max() function.

numbers = [14, 67, 23, 89, 45, 12, 90, 34]

# Start by assuming the first number is the largest
largest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num

print(f"List: {numbers}")
print(f"The largest number is: {largest}")


'''

List: [14, 67, 23, 89, 45, 12, 90, 34]
The largest number is: 90

'''
