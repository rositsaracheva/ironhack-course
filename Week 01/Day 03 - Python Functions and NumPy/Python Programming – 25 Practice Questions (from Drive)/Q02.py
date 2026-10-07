# Question 2: Variables, Input & Operators
# Write a program that asks the user for two numbers and displays their
# addition, subtraction, multiplication, and division.

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

addition = num1 + num2
subtraction = num1 - num2
multiplication = num1 * num2
division = num1 / num2

print(f"Addition: {num1} + {num2} = {addition}")
print(f"Subtraction: {num1} - {num2} = {subtraction}")
print(f"Multiplication: {num1} * {num2} = {multiplication}")
print(f"Division: {num1} / {num2} = {division}")


'''

Enter first number: 2
Enter second number: 4
Addition: 2.0 + 4.0 = 6.0
Subtraction: 2.0 - 4.0 = -2.0
Multiplication: 2.0 * 4.0 = 8.0
Division: 2.0 / 4.0 = 0.5

'''