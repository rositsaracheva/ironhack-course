# Question 7: if / elif / else
# Write a program that asks for a person's age and determines whether they are a child, teenager, or adult.

age = int(input("Enter your age: "))

if age < 13:
    print("You are a child.")
elif age <= 19:
    print("You are a teenager.")
else:
    print("You are an adult.")


'''

Enter your age: 16
You are a teenager.

'''
