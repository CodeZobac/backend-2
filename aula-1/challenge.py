import time
def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swapping occurred in this pass, the array is already sorted
        if not swapped:
            break
    
    return arr

if __name__ == "__main__":
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],  # Random array
        [1, 2, 3, 4, 5],  # Already sorted array
        [5, 4, 3, 2, 1]   # Reverse sorted array
    ]
    
    for i, test in enumerate(test_cases):
        start_time = time.time()
        print(f"Test case {i+1}: {test}")
        bubble_sort(test)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to sort: {elapsed_time:.10f} seconds")
        print(f"Sorted result: {test}")
        print()