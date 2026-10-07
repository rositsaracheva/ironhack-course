# 1. Create the tuple
store_location = ("LDN-01", "London", "South")

# 2. Print each value by position
print("Store ID:", store_location[0])
print("City:", store_location[1])
print("Region:", store_location[2])

# 3. Trying to change "London" to "Leeds":
# store_location[1] = "Leeds"
# Note: This causes a TypeError because tuples are immutable (cannot be changed).

