# Question 5: if / elif / else
# Write a program that asks the user for a number and determines whether
# it is positive, negative, or zero.

number = float(input("Enter a number: "))

if number > 0:
    print(f"{number} is positive.")
elif number < 0:
    print(f"{number} is negative.")
else:
    print("The number is zero.")


'''

Enter a number: 15
15.0 is positive.

'''
