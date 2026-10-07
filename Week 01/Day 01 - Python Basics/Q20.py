'''Q. 20 — Test Boundary Values'''

'''Test 1: 99.99'''
amount = 99.99
is_high_value = amount >= 100
print(f"Amount: {amount:.2f} -> High value: {is_high_value}")

'''Test 2: 100.00'''
amount = 100.00
is_high_value = amount >= 100
print(f"Amount: {amount:.2f} -> High value: {is_high_value}")

'''Test 3: 100.01'''
amount = 100.01
is_high_value = amount >= 100
print(f"Amount: {amount:.2f} -> High value: {is_high_value}")

'''
Results:
- 99.99  -> False
- 100.00 -> True
- 100.01 -> True

Why testing 100.00 is important:
100.00 is the exact boundary threshold. Testing it verifies that the boundary is inclusive (using '>=' instead of '>'). 
If the code mistakenly used 'amount > 100', both 99.99 (False) and 100.01 (True) would still pass, but 100.00 would fail by returning False instead of True. Testing the exact boundary catches these comparison errors.
'''
