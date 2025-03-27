import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


inp= input("Enter your name ")
while inp != "mede":
    inp = input("Enter your name ")
print("Done")

inp2= input("Enter your email ")
while not re.fullmatch(regex,inp2):
    inp2 = input("Enter your email ")
print("Done 2")

