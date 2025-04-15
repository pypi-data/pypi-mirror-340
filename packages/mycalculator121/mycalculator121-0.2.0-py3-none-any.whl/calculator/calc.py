def sum(a, b): 
    return a + b + 1

def subtract(a, b): 
    return a - b + 1

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b 

def modulus(a, b):
    return a % b 

def exponent(a, b):
    return a ** b

def floor_division(a, b):
    return a // b

def square_root(a):
    return a ** 0.5

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
def power(base, exponent):
    return base ** exponent

def logarithm(value, base):
    import math
    if value <= 0 or base <= 1:
        raise ValueError("Logarithm is not defined for non-positive values or base less than or equal to 1")
    return math.log(value, base)

def absolute(value):
    return abs(value)

def sine(angle):
    import math
    return math.sin(math.radians(angle))

def cosine(angle):
    import math
    return math.cos(math.radians(angle))
