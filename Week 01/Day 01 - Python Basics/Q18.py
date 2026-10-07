quantity = int(input("Quantity: "))
discount_percent = float(input("Discount %: "))
 
valid_quantity = quantity > 0
valid_discount = (
    discount_percent >= 0
    and discount_percent <= 100
)
all_valid = valid_quantity and valid_discount
 
print("Valid quantity:", valid_quantity)
print("Valid discount:", valid_discount)
print("All values valid:", all_valid)


'''TERMINAL TEST:

Quantity: 2
Discount %: 20
Valid quantity: True
Valid discount: True '''
