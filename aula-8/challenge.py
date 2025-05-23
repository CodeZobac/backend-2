# Challenge: Tests for a recursive factorial function using pytest parametrization
import pytest

def factorial(n):
    """Calculate factorial of n recursively."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    return base ** exponent

if __name__ == "__main__":
    # Example usage
    print(f"factorial(5) = {factorial(5)}")
    print(f"fibonacci(7) = {fibonacci(7)}")
    print(f"is_prime(17) = {is_prime(17)}")
    print(f"power(2, 3) = {power(2, 3)}")