store_ids = ["LDN-01", "MAN-02", "LDN-01", "BRS-03", "MAN-02"]

# Convert the list to a set to remove duplicates
unique_store_ids = set(store_ids)

# 1. Print the original count
print("Original count:", len(store_ids))

# 2. Print the unique count
print("Unique count:", len(unique_store_ids))

# 3. Print the unique values
print("Unique values:", unique_store_ids)

# OUTPUT:

'''

Original count: 5
Unique count: 3
Unique values: {'LDN-01', 'MAN-02', 'BRS-03'}

'''

