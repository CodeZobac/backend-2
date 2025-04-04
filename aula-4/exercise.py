#!/usr/bin/env python3
"""
Exercise: Multi-processing Factorial Computation

This program demonstrates how to use multi-processing to compute
factorials of multiple numbers concurrently.
"""

import multiprocessing
import time


def factorial(n):
    """Recursive factorial function."""
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


def compute_factorial(number):
    """Compute factorial and return result with the input number."""
    result = factorial(number)
    return f"Factorial of {number} is {result}"


def main():
    # List of numbers to compute factorial for
    numbers = [5, 10, 15, 20, 25]
    
    # Create a process for each number
    processes = []
    
    start_time = time.time()
    
    # Spawn a process for each number
    for num in numbers:
        process = multiprocessing.Process(
            target=lambda n: print(compute_factorial(n)),
            args=(num,)
        )
        processes.append(process)
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    # This guard is important for multiprocessing to work correctly
    main()