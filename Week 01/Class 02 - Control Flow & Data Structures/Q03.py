statuses = [
    "complete",
    "cancelled",
    "complete",
    "complete",
]
 
amounts = [
    45.50,
    18.00,
    62.25,
    30.00,
]

# Start calculator at 0
total = 0

# Go through row 0, 1, 2, 3

for i in range(len(statuses)):   # Check if the status at this row is complete
    
    if statuses[i] == "complete":
        total = total + amounts[i]
print("Total:" , total)

# Output: Total: 137.75

