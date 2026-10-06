
order_ids = [301, 302, 303, 304, 305]
target_id = 303

# Loop through each order ID:

for order_id in order_ids:

# Check if it matches the target:

    if order_id == target_id:

# Print it and exit immediately: 

        print("target id reached:", order_id ,"we will stop here.")
        break

# Result: target id reached: 303 we will stop here.