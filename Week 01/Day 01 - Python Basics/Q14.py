''' A: city = "London
print(city) -> SyntaxError'''

city = "London"
print(city)

'''B: amount = 25
print(amunt) -> NameError'''

amount = 25
print(amount)

''' C: amount = "25"
print(amount + 10) -> TypeError'''

amount = "25"
print(int(amount) + 10)

'''D: quantity = int("three") -> ValueError'''

quantity = int("3")



