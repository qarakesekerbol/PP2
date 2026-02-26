#1
import math
degree = float(input("Enter angle in degrees: "))
radian = degree * (math.pi / 180)
print("Angle in radians:", radian)

#2
height = int(input())
base1 = int(input())
base2 = int(input())
area = 0.5 * (base1 + base2) * height
print("Area of trapezoid:", area)

#3
import math
n = int(input())
s = int(input())
area = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)

#4

base = int(input())
height = int(input())
area = base * height
print("Area of parallelogram:", float(area))