# Exercise: Basic Testing with pytest
# Write a Python function that multiplies two numbers and create a corresponding pytest test

def multiply(a, b):
    """Multiply two numbers together."""
    return a * b

def add(a, b):
    """Add two numbers together."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

if __name__ == "__main__":
    # Example usage
    print(f"multiply(3, 4) = {multiply(3, 4)}")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"subtract(10, 4) = {subtract(10, 4)}")