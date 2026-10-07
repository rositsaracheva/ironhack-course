amounts = [45.50, -5.00, 18.00, 0, 62.25]

total = 0.0

for amount in amounts:
    # Skip amounts that are 0 or negative
    if amount <= 0:
        continue
    
    # Print only valid amounts
    print(f"Valid amount: {amount:.2f}")
    total += amount

# Print the total after checking all items
print(f"Total: {total:.2f}")


# OUTPUT: 

'''

Valid amount: 45.50
Valid amount: 18.00
Valid amount: 62.25
Total: 125.75

'''