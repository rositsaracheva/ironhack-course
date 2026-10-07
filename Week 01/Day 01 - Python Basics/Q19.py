city = input("City: ")
amount = float(input("Amount: "))
 
is_high_value = amount >= 100
 
print(
    f"{city} | £{amount:.2f} | "
    f"High value: {is_high_value}"
)