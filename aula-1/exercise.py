import time

def factorial(n):    
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)


if __name__ == "__main__":
    test_values = [0, 1, 5, 10]
    for val in test_values:
        start_time = time.time()

        result = factorial(val)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to compute factorial({val}): {elapsed_time:.10f} seconds")
        print(f"factorial({val}) = {result}")

