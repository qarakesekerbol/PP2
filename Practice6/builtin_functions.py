#1
numbers = [1, 2, 3, 4, 5]

# map: квадрат
squared = list(map(lambda x: x**2, numbers))
print(squared)

# filter: тек жұп сандар
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

#2
from functools import reduce

numbers = [1, 2, 3, 4, 5]

sum_all = reduce(lambda x, y: x + y, numbers)
print(sum_all)

#3
names = ["Ali", "Dana", "Aruzhan"]
scores = [85, 90, 95]

# enumerate
for index, name in enumerate(names):
    print(index, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

#4
value = "123"

# type check
print(type(value))

# convert to int
num = int(value)
print(num, type(num))

# convert to float
num_float = float(value)
print(num_float, type(num_float))

# convert to string
num_str = str(num)
print(num_str, type(num_str))