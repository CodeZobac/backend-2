#!/usr/bin/env python3
"""
Challenge: Multi-process Sum of Squares

This program divides a large list of numbers into sublists and concurrently
computes the sum of squares for each sublist using multiprocessing.Pool.
"""

import multiprocessing
import time
import math
import random


def sum_of_squares(numbers):
    """
    Calculate the sum of squares for a list of numbers.
    """
    result = sum(num ** 2 for num in numbers)
    return result


def split_list(full_list, num_chunks):
    """
    Split a list into approximately equal-sized chunks.
    """
    chunk_size = math.ceil(len(full_list) / num_chunks)
    return [full_list[i:i + chunk_size] for i in range(0, len(full_list), chunk_size)]


def main():
    # Generate a large list of random numbers
    list_size = 10_000_000
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    
    print(f"Generating a list of {list_size:,} random numbers...")
    numbers = [random.randint(1, 100) for _ in range(list_size)]
    
    # Split the list into chunks, one for each process
    chunks = split_list(numbers, num_processes)
    print(f"Dividing list into {len(chunks)} chunks for processing")
    
    start_time = time.time()
    
    # Sequential calculation (for comparison)
    seq_start = time.time()
    sequential_result = sum_of_squares(numbers)
    seq_end = time.time()
    print(f"Sequential result: {sequential_result:,}")
    print(f"Sequential time: {seq_end - seq_start:.4f} seconds")
    
    # Parallel calculation using Pool
    pool_start = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Map each chunk to the sum_of_squares function
        results = pool.map(sum_of_squares, chunks)
        # Sum the results from all processes
        parallel_result = sum(results)
    pool_end = time.time()
    
    print(f"Parallel result: {parallel_result:,}")
    print(f"Parallel time: {pool_end - pool_start:.4f} seconds")
    
    # Verify results match
    assert sequential_result == parallel_result, "Results don't match!"
    
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.4f} seconds")
    print(f"Speedup: {(seq_end - seq_start) / (pool_end - pool_start):.2f}x")


if __name__ == "__main__":
    # This guard is important for multiprocessing to work correctly
    main()