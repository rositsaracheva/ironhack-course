# Accepted data from Q17:
accepted_orders = [
    {"order_id": 401, "city": "London", "amount_gbp": 45.50},
    {"order_id": 403, "city": "Leeds", "amount_gbp": 30.00},
]

# 1. Start with an empty dictionary
city_revenue = {}

# 2. Sum revenue by city
for order in accepted_orders:
    city = order["city"]
    amount = order["amount_gbp"]
    
    if city in city_revenue:
        city_revenue[city] += amount
    else:
        city_revenue[city] = amount

# 3. Print the resulting dictionary
print("Revenue by city:", city_revenue)


# OUTPUT: Revenue by city: {'London': 45.5, 'Leeds': 30.0}
