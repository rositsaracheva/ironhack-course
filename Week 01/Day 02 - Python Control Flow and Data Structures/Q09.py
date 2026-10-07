stores = ["London", "Manchester", "Bristol"] # Starting list: index 0 is London, 1 is Manchester, 2 is Bristol


# Add Leeds
stores.append("Leeds") # List is now: ["London", "Manchester", "Bristol", "Leeds"]

# Change Bristol to Birmingham (Bristol is at index 2)
stores[2] = "Birmingham" # List is now: ["London", "Manchester", "Birmingham", "Leeds"]

# Remove Manchester
stores.remove("Manchester") # List is now: ["London", "Birmingham", "Leeds"]

# Print the final list
print(stores)

# OUTPUT : ['London', 'Birmingham', 'Leeds']