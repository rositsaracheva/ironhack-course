orders = [
    {"order_id": 401, "city": "London", "amount_gbp": 45.50},
    {"order_id": 402, "city": "Manchester", "amount_gbp": -5.00},
    {"order_id": 401, "city": "London", "amount_gbp": 45.50},
    {"order_id": 403, "city": "Leeds", "amount_gbp": 30.00},
]

# 1. Create the containers

accepted_orders = []
rejected_orders = []
seen_order_ids = set()

# 2. Filter and clean the orders

for order in orders:
    order_id = order["order_id"]
    amount = order["amount_gbp"]
    
    # Check if duplicate or non-positive

    if order_id in seen_order_ids or amount <= 0:
        rejected_orders.append(order)
    else:
        accepted_orders.append(order)
        seen_order_ids.add(order_id)

# 3. Print results

print("Accepted orders:", accepted_orders)
print("Rejected orders:", rejected_orders)
print("Seen order IDs:", seen_order_ids)

# OUTPUT:

'''

Accepted orders: [{'order_id': 401, 'city': 'London', 'amount_gbp': 45.5}, {'order_id': 403, 'city': 'Leeds', 'amount_gbp': 30.0}]
Rejected orders: [{'order_id': 402, 'city': 'Manchester', 'amount_gbp': -5.0}, {'order_id': 401, 'city': 'London', 'amount_gbp': 45.5}]
Seen order IDs: {401, 403}

'''

