# Question 18: Lists + Loops
# Given a list of numbers, calculate the total without using the built-in sum() function.

numbers = [10, 20, 30, 40, 50]

total = 0

for num in numbers:
    total += num

print(f"List of numbers: {numbers}")
print(f"Total calculated with loop: {total}")


'''

List of numbers: [10, 20, 30, 40, 50]
Total calculated with loop: 150

'''
