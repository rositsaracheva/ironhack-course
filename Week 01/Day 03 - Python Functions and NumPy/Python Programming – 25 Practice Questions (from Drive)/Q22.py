# Question 22: Functions
# Write a function check_even_odd(number) that accepts a number and returns "Even" or "Odd".

def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Test the function:
test_num = int(input("Enter a number to check: "))
result = check_even_odd(test_num)
print(f"The number {test_num} is: {result}")


'''

Enter a number to check: 7
The number 7 is: Odd

'''
