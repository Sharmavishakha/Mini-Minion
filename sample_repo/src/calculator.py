"""Simple calculator implementation.

Provides basic arithmetic operations: add, subtract, multiply, divide, and power.
The original file contained intentional bugs for the challenge; they have been fixed.
"""

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b (a - b)."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


def power(base, exp):
    """Return base raised to the power of exp.

    Implements exponentiation via iterative multiplication.
    """
    result = 1
    for _ in range(exp):
        result *= base
    return result
