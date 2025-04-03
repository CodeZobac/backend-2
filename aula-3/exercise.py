import threading
import time

def print_letters():
    """Thread function that prints letters A through J with a small delay."""
    for letter in 'ABCDEFGHIJ':
        print(f"Letter: {letter}")
        time.sleep(0.5)

def print_numbers():
    """Thread function that prints numbers 1 through 10 with a small delay."""
    for number in range(1, 11):
        print(f"Number: {number}")
        time.sleep(0.5)

def main():
    # Create threads
    letter_thread = threading.Thread(target=print_letters)
    number_thread = threading.Thread(target=print_numbers)
    
    # Start threads
    letter_thread.start()
    number_thread.start()
    
    # Wait for both threads to complete
    letter_thread.join()
    number_thread.join()
    
    print("All threads have finished execution.")

if __name__ == "__main__":
    main()