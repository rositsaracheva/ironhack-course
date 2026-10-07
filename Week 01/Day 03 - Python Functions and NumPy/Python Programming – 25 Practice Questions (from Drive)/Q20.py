# Question 20: Lists + Loops
# Given a list of student marks, use a loop to count how many students
# passed and how many failed. A mark of 40 or above is considered a pass.

marks = [55, 38, 72, 40, 29, 85, 39, 90, 62]

passed_count = 0
failed_count = 0

for mark in marks:
    if mark >= 40:
        passed_count += 1
    else:
        failed_count += 1

print(f"Student marks: {marks}")
print(f"Number of students who passed: {passed_count}")
print(f"Number of students who failed: {failed_count}")


'''

Student marks: [55, 38, 72, 40, 29, 85, 39, 90, 62]
Number of students who passed: 6
Number of students who failed: 3

'''
