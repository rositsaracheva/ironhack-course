# Question 14: for Loops
# Write a program to display the multiplication table of a number entered by the user.

num = int(input("Enter a number: "))

print(f"--- Multiplication Table for {num} ---")
for i in range(1, 11):
    result = num * i
    print(f"{num} x {i} = {result}")


'''

Enter a number: 5
--- Multiplication Table for 5 ---
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50

'''
