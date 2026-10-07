# 0CTOBER 7 -  DAY 3

# DEFINE A FUNCTION THAT SQUARES THE ARGUMENT:

'''

def square(x):
    return x ** 2

result1 = square(4)
print("Square of 4 is:", result1)

result2 = square(5)
print("Square of 5 is:", result2)

--- OUTPUT ---

Square of 4 is: 16
Square of 5 is: 25

'''


# CREATE A FUNCTION WHERE THERE IS A MULTIPLICATION OF VALUES AND A DIVISION:

# Function takes 3 numbers: a, b, and c
# Test with numbers: (10 * 6) / 2 = 60 / 2 = 30.0

'''
def multiply_and_divide(a, b, c):  
    return (a * b) / c

result = multiply_and_divide(10, 6, 2)
print("Result:", result) 

OUTPUT: 30.0

'''

# CREATE A FUNCTION WHICH TAKES THE SIDE OF A SQUARE AND RETURN THE AREA OF THE SQUARE,TAKE THE INPUT FROM THE USER :

# 1. Define the function
# 2. Take input from the user (convert to float)
# 3. Call the function
# 4. Print the result

'''

def calculate_square_area(side):
    return side ** 2


user_side = float(input("Enter the side length of the square: "))


area = calculate_square_area(user_side)

# 4. Print the result
print(f"The area of the square is: {area:.2f}") 

--- OUTPUT ---

# Enter the side length of the square: 5
#The area of the square is: 25.00

'''

# CALCULATE THE AREA OF A CIRCLE, TAKE INPUT FROM USER:
'''

def calculate_circle_area(radius):
    pi = 3.14159
    return pi * (radius ** 2)
user_radius = float(input("Enter the radius of the circle, NOW! :): "))
area = calculate_circle_area(user_radius)
print(f"The area of the circle is: {area:.2f}")

# Enter the radius of the circle: 4
#The area of the circle is: 50.27

'''

# MAKE A MENU CHOICE TO THE USER, MULTIPLE CHOICE (DEFINE CIRCLE,SQUARE AND RECTANGLE): 

# 1. Define the 3 shape functions

'''

def calculate_square_area(side):
    return side ** 2

def calculate_circle_area(radius):
    pi = 3.14159
    return pi * (radius ** 2)

def calculate_rectangle_area(width, height):
    return width * height


# 2. Display the Menu
print("--- AREA CALCULATOR ---")
print("1. Square Area")
print("2. Circle Area")
print("3. Rectangle Area")

# 3. Get user's choice
choice = input("Choose an option (1, 2, or 3): ")

# 4. Handle choices with if / elif / else
if choice == "1":
    side = float(input("Enter the side of the square: "))
    area = calculate_square_area(side)
    print(f"The area of the square is: {area:.2f}")

elif choice == "2":
    radius = float(input("Enter the radius of the circle: "))
    area = calculate_circle_area(radius)
    print(f"The area of the circle is: {area:.2f}")

elif choice == "3":
    width = float(input("Enter the width of the rectangle: "))
    height = float(input("Enter the height of the rectangle: "))
    area = calculate_rectangle_area(width, height)
    print(f"The area of the rectangle is: {area:.2f}")

else:
    print("Invalid choice! Please select 1, 2, or 3.") '''


# NumPy Arrays — Creating Arrays

'''

import numpy as np

a = np.array([10, 20, 30])
b = np.zeros(4)
c = np.ones((2, 3))
d = np.arange(0, 10, 2)

print("a (array):")
print(a)

print("\nb (zeros):")
print(b)

print("\nc (ones 2x3):")
print(c)

print("\nd (arange):")
print(d)

'''
'''
import numpy as np
 
arr = np.array([[10, 20, 30],
                [40, 50, 60]])
 
print(arr[0, 1])   # row 0, col 1
print(arr[1][2])   # row 1, col 2
print(arr[-1, -1]) 

#output

20
60
60

'''
'''
import numpy as np
 
a = np.array([10, 20, 30])
b = np.array([1, 2, 3])
 
print(a + 5)
print(a * 2)
print(a + b)

OUTPUT: 

[15 25 35]
[20 40 60]
[11 22 33]

'''
'''
data = np.array([[10, 20, 30],
                 [40, 50, 60],
                 [70, 80, 90]])
 
print("Total sum:", data.sum())
print("Column-wise mean:", data.mean(axis=0))
print("Row-wise max:", data.max(axis=1))
print("Overall min:", np.min(data))

'''





