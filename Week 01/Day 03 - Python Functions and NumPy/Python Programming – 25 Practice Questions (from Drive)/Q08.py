# Question 8: if / elif / else
# Write a program that accepts marks from 0 to 100 and displays the appropriate grade:
# 90–100 -> A
# 80–89  -> B
# 70–79  -> C
# 60–69  -> D
# Below 60 -> F

marks = float(input("Enter marks (0 to 100): "))

if marks >= 90:
    print("Grade: A")
elif marks >= 80:
    print("Grade: B")
elif marks >= 70:
    print("Grade: C")
elif marks >= 60:
    print("Grade: D")
else:
    print("Grade: F")


'''

Enter marks (0 to 100): 85
Grade: B

'''
