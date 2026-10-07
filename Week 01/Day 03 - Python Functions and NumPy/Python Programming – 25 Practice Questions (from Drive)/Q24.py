# Question 24: Functions
# Write a function count_greater(numbers, value) that accepts a list of numbers
# and a value, and returns how many numbers in the list are greater than that value.

def count_greater(numbers, value):
    count = 0
    for num in numbers:
        if num > value:
            count += 1
    return count

# Test the function:
sample_numbers = [10, 25, 40, 5, 80, 15]
threshold = 20

result = count_greater(sample_numbers, threshold)
print(f"List: {sample_numbers}")
print(f"Numbers greater than {threshold}: {result}")


'''

List: [10, 25, 40, 5, 80, 15]
Numbers greater than 20: 3

'''
