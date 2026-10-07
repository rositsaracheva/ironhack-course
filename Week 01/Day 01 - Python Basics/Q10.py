status_1 = "complete"
amount_gbp_1 = 45.50

status_2 = "cancelled"
amount_gbp_2 = 45.50

status_3= "complete"
amount_gbp_3 = -5.00

print(status_1 == "complete" and amount_gbp_1 > 0) # True
print(status_2 == "complete" and amount_gbp_2 > 0) # False
print(status_3 == "complete" and amount_gbp_3 > 0) # False