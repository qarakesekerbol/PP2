#1
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)  
        self.grade = grade

s = Student("Ali", 11)
print(s.name, s.grade)

#2
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        super().speak()  # ата-ананың әдісі
        print("Dog says Woof")

d = Dog()
d.speak()

#3
class Employee:
    def get_salary(self):
        return 1000

class Manager(Employee):
    def get_salary(self):
        base = super().get_salary()
        return base + 500

m = Manager()
print(m.get_salary())


