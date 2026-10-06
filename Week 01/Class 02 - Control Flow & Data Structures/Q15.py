cities = ["London", "Manchester", "London", "Leeds", "London", "Manchester"]

# 1. Start with an empty dictionary
city_counts = {}

# 2. Count each city
for city in cities:
    if city in city_counts:
        city_counts[city] += 1
    else:
        city_counts[city] = 1

# 3. Print the final counts
print(city_counts)


'''

{'London': 3, 'Manchester': 2, 'Leeds': 1}

'''