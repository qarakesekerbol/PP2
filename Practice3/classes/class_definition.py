#1
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello,", self.name)

p = Person("Ali")
p.greet()

#2
class Car:
    def __init__(self, brand):
        self.brand = brand

    def drive(self):
        print(self.brand, "is driving")

# Қолдану
c = Car("Toyota")
c.drive()

#3
class Calculator:
    def add(self, a, b):
        return a + b

# Қолдану
calc = Calculator()
print(calc.add(5, 3))

#4
class Cat:
    def __init__(self, color):
        self.color = color

    def meow(self):
        print("Meow! My color is", self.color)

# Қолдану
cat1 = Cat("black")
cat1.meow()

