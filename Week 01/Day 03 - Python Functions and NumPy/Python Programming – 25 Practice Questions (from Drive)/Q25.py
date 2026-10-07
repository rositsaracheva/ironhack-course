# Question 25: Combined Challenge
# Write a function called analyze_numbers(numbers) that accepts a list of numbers and calculates:
# - Total number of values
# - Sum of the values
# - Average
# - Largest value
# - Smallest value
# - Number of even values
# - Number of odd values

def analyze_numbers(numbers):
    total_count = len(numbers)
    
    total_sum = 0
    largest = numbers[0]
    smallest = numbers[0]
    even_count = 0
    odd_count = 0
    
    for num in numbers:
        # Accumulate total sum
        total_sum += num
        
        # Check for largest and smallest
        if num > largest:
            largest = num
        if num < smallest:
            smallest = num
            
        # Count even and odd numbers
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
            
    average = total_sum / total_count
    
    return {
        "Total values": total_count,
        "Sum": total_sum,
        "Average": average,
        "Largest": largest,
        "Smallest": smallest,
        "Even count": even_count,
        "Odd count": odd_count
    }

# Test the function:
data = [12, 45, 7, 89, 23, 56, 34, 91, 10]
analysis = analyze_numbers(data)

print(f"Dataset: {data}\n")
for key, value in analysis.items():
    print(f"{key}: {value}")


'''

Dataset: [12, 45, 7, 89, 23, 56, 34, 91, 10]

Total values: 9
Sum: 367
Average: 40.77777777777778
Largest: 91
Smallest: 7
Even count: 4
Odd count: 5

'''
