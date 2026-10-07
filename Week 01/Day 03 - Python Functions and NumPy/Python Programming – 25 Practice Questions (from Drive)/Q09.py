# Question 9: if / elif / else
# Write a program that asks for three numbers and finds the largest number.

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
num3 = float(input("Enter third number: "))

if num1 >= num2 and num1 >= num3:
    largest = num1
elif num2 >= num1 and num2 >= num3:
    largest = num2
else:
    largest = num3

print(f"The largest number is: {largest:.2f}")


'''

Enter first number: 12
Enter second number: 45
Enter third number: 30
The largest number is: 45.00

'''
