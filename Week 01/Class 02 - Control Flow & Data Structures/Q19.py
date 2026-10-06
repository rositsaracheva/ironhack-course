amounts = [10, -5, 20, 0, 30, 40]

valid_count = 0

for amount in amounts:
    # 1. Skip invalid values (0 or negative)
    if amount <= 0:
        continue
    
    # 2. Process valid value
    print("Processed:", amount)
    valid_count += 1
    
    # 3. Stop after three valid values
    if valid_count == 3:
        break

# OUTPUT: 

'''
Processed: 10
Processed: 20
Processed: 30

'''