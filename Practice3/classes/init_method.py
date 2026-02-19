#1
class Book:
    def __init__(self, title):
        self.title = title

b = Book("Harry Potter")
print(b.title)

#2
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s = Student("Ali", 16)
print(s.name, s.age)

#3
class Phone:
    def __init__(self, brand, price=0):
        self.brand = brand
        self.price = price

p1 = Phone("iPhone")
p2 = Phone("Samsung", 300000)

print(p1.brand, p1.price)
print(p2.brand, p2.price)
