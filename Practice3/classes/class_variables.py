#1
class Student:
    school_name = "NIS"   # class variable

    def __init__(self, name):
        self.name = name

s1 = Student("Ali")
s2 = Student("Dana")

print(s1.school_name)
print(s2.school_name)

#2
class Product:
    tax_rate = 0.1   # 10%

    def __init__(self, price):
        self.price = price

    def final_price(self):
        return self.price * (1 + Product.tax_rate)

p = Product(1000)
print(p.final_price())

#3
class Phone:
    discount = 0.2   # 20% жеңілдік

    def __init__(self, price):
        self.price = price

Phone.discount = 0.3  # бүкіл класс үшін өзгерді

p1 = Phone(100000)
print(p1.price * (1 - Phone.discount))
