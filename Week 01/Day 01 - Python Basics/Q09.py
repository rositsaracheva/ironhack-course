# 1. Ask the user for input and convert to float
order_amount = float(input("Enter the order amount: "))

# 2. Check if the amount is at least 100 (creates a True/False boolean)
is_high_value = order_amount >= 100

# 3. Print the result
print(is_high_value)


# OUTPUT -TERMINAL:

# Enter the order amount: 45.50 --> False

# Enter the order amount: 125 --> True