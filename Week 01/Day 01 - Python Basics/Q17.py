order_id = input("Order ID: ")
city = input("City: ")
unit_price = float(input("Unit price: "))
quantity = int(input("Quantity: "))
discount_percent = float(input("Discount %: "))
 
subtotal = unit_price * quantity
discount_amount = subtotal * discount_percent / 100
final_total = subtotal - discount_amount
 
print(
    f"Order {order_id} | {city} | "
    f"Subtotal £{subtotal:.2f} | "
    f"Discount £{discount_amount:.2f} | "
    f"Final £{final_total:.2f}"
)

''' TERMINAL TEST:

Order ID: 1
City: Alicante
Unit price: 400
Quantity: 2
Discount %: 20
Order 1 | Alicante | Subtotal £800.00 | Discount £160.00 | Final £640.00 '''


