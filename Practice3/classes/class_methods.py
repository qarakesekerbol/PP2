#1
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        celsius = (fahrenheit - 32) * 5 / 9
        return cls(celsius)

t = Temperature.from_fahrenheit(68)
print(round(t.celsius, 2))

#2
class User:
    minimum_age = 18

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def is_allowed(cls, age):
        return age >= cls.minimum_age

print(User.is_allowed(20))  # True
print(User.is_allowed(15))  # False

#3
class Currency:
    rate = 500  # 1$ = 500 тг

    @classmethod
    def convert_to_tenge(cls, dollars):
        return dollars * cls.rate

print(Currency.convert_to_tenge(10))


