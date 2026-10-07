# We first define the list:
amounts = [24.50, 55.00, 120.00, 49.99, 99.50]

# Loop through each element:
for amount in amounts:
    if amount >= 100:
        print(f"{amount:.2f} - High") # I want to see the result together with the amount with 2 decimal places.
    elif amount >=50:
        print(f"{amount:.2f} - Medium") # I want to see the result together with the amount with 2 decimal places.
    else:
        print(f"{amount:.2f} - Low") # I want to see the result together with the amount with 2 decimal places.

# OUTPUT: 

''' 

24.50 - Low
55.00 - Medium
120.00 - High
49.99 - Low
99.50 - Medium

'''

