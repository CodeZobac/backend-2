# Backend II
## Session 1: Fundamentals of Big O Notation in Python Performance

**Goal:**
Understand how algorithm complexity is measured with Big O notation and why it matters for performance in Python.

**Definition:**
Big O notation expresses the upper bound of an algorithm’s runtime relative to its input size. It helps you compare algorithms and identify potential bottlenecks. Use cases include analysing search, sort, or any iterative processes. In Python, knowing Big O is essential for writing efficient code when dealing with large datasets.

**Documentation Reference:**
- https://docs.python.org/3/tutorial/datastructures.html
- https://en.wikipedia.org/wiki/Big_O_notation
- https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/
- https://www.bigocheatsheet.com/

### Tutorial:

- Write a simple linear search function:
```py
def linear_search(lst, target):
    for item in lst:
        if item == target:
            return True
    return False
```

- Explanation: This function’s runtime grows linearly with the size of the list, hence O(n).

- Comparison: Briefly discuss how a binary search (O(log n)) differs in performance.

### Exercise:

- Problem: Write a recursive function to calculate factorial and determine its time complexity.
- Steps to Solve:
    - Define the recursive factorial function.
    - Analyse how many times the function is called relative to the input.

### Challenge:

- Problem: Optimise a bubble sort algorithm so that it stops early if the list is already sorted.
> Hint: Use a flag to detect whether a swap occurred.

## Session 2: Implementing Design Patterns in Python for Robust Architecture

**Goal:**
Learn key design patterns and how to implement them in Python to build maintainable and robust applications.

**Definition:**
Design patterns are standard solutions to common software design problems. They promote reusability and cleaner code structure. Use cases include managing shared resources (Singleton), abstracting object creation (Factory), and handling events (Observer). Mastery of these patterns leads to clearer communication among developers and more scalable applications.

**Documentation Reference:**
- https://refactoring.guru/design-patterns/python
- https://www.tutorialspoint.com/python_design_patterns/index.htm

### Tutorial:
- Introduction to Singleton: Explain why you might need only one instance of a class.
```py
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)
```
- Explanation: Both instances refer to the same object.
- Discussion: Briefly mention other patterns (Factory, Observer) for context.

### Exercise:

- Problem: Implement the Factory pattern to create shape objects (e.g., Circle and Square).

- Steps to Solve:
    - Define an abstract Shape class.
    - Create concrete classes for Circle and Square.
    - Write a factory function to return the correct object.

### Challenge:

- Problem: Implement the Observer pattern to notify multiple observers when a subject’s state changes.
- Hint: Create a Subject class that maintains a list of observers.

## Session 3: Mastering Multi-threading in Python

**Goal:**
Learn how to run code concurrently using threads to improve performance for I/O-bound tasks.

**Definition:**
Multi-threading splits a program into multiple threads running in parallel. In Python, this is ideal for I/O-bound operations because threads share the same memory space. Use cases include network operations, file I/O, and handling multiple user requests. Despite the Global Interpreter Lock (GIL), multi-threading remains effective for many practical scenarios.

**Documentation Reference:**
- https://docs.python.org/3/library/threading.html
- https://realpython.com/intro-to-python-threading/
- https://www.tutorialspoint.com/python/python_multithreading.htm

### Tutorial:

- Introduction: Explain the threading module.

```py
import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(1)

thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()
```
- Explanation: This runs the print_numbers function in a separate thread.
- Discussion: Mention when to use threads (e.g., I/O-bound tasks).

### Exercise:

- Problem: Create two threads that print letters and numbers concurrently.
- Steps to Solve:
    - Define two functions—one for letters and one for numbers.
    - Create and start a thread for each function.

### Challenge:

- Problem: Create a multi-threaded program that downloads multiple files concurrently from given URLs.
- Hint: Use the threading module along with urllib.request.urlretrieve.


## Session 4: Multi-processing in Python for Scalability
**Goal:**
Understand how to run tasks concurrently in separate processes to boost performance in CPU-bound tasks.

**Definition:**
Multi-processing uses separate processes with their own memory space, bypassing the Global Interpreter Lock (GIL). This technique is ideal for CPU-intensive tasks such as heavy computations or large data processing, where parallel execution on multiple cores can lead to significant speed improvements. It is commonly used in scenarios that require isolated execution environments.

**Documentation Reference:**

- https://docs.python.org/3/library/multiprocessing.html
- https://realpython.com/python-multiprocessing/
- https://www.geeksforgeeks.org/multiprocessing-python-set-1/

**Tutorial:**
- Introduction: Explain the difference between threading and multi-processing.
- Step-by-Step Example:
    - Import the multiprocessing module.
    -  Define a simple function (e.g., compute a square).
    - Create and start multiple processes.
```py
import multiprocessing
import time

def compute_square(n):
    time.sleep(1)  # Simulate a heavy computation
    print(f"Square of {n} is {n*n}")

if __name__ == "__main__":
    numbers = [2, 3, 4, 5]
    processes = []
    for number in numbers:
        p = multiprocessing.Process(target=compute_square, args=(number,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

```
- Explanation: Each process runs independently, and joining ensures all complete before the script ends.

### Exercise:

- Problem: Create a program that concurrently computes the factorial of several numbers using multi-processing.
- Steps to Solve:
    - Define a recursive factorial function.
    - Spawn a process for each number in a list.

### Challenge:

- Problem: Create a multi-process program that divides a large list of numbers into sublists and computes the sum of squares for each sublist concurrently.
- Hint:
  Use the Pool class from the multiprocessing module.

## Session 5: Asynchronous Programming in Python with asyncio and FastAPI

**Goal:**
Learn to write non-blocking code using asyncio and integrate it into a FastAPI endpoint.

**Definition:**
Asynchronous programming allows concurrent execution of tasks without waiting for each to complete sequentially. In Python, the asyncio library provides tools to write such code, which is especially useful for I/O-bound operations like web requests or database calls. This enables scalable web services by handling multiple requests simultaneously.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio.html
- https://fastapi.tiangolo.com/async/
- https://realpython.com/async-io-python/

**Tutorial:**
- Setup FastAPI:
```bash
poetry add fastapi uvicorn
```
- Step-by-Step Example:

    - Create an asynchronous function using async def and await.
    - Define a FastAPI endpoint that calls this async function.
```py
    from fastapi import FastAPI
    import asyncio

    app = FastAPI()

    async def simulated_io_task():
        await asyncio.sleep(1)
        return "Data fetched!"

    @app.get("/async-data")
    async def get_data():
        result = await simulated_io_task()
        return {"message": result}

    # Run using: uvicorn filename:app --reload
```
- Explanation: The endpoint /async-data executes the async task without blocking other requests.

### Exercise:

- Problem: Create a FastAPI endpoint that concurrently fetches data from two simulated sources using asyncio.gather.

    - Steps to Solve:
        - Define two async functions that simulate data fetching.
        - Use asyncio.gather to run them concurrently.


### Challenge:

- Problem:Develop an asynchronous web scraper that fetches HTML content from multiple URLs concurrently using aiohttp.
    - Hint: Use the aiohttp library with asyncio.gather.

## Session 6: Advanced Async Patterns and Concurrency Techniques

**Goal:**
Explore advanced asynchronous programming concepts to manage tasks, handle timeouts, and coordinate concurrent operations efficiently.

**Definition:**
Beyond basic async functions, advanced patterns include task scheduling, handling cancellations, and synchronising shared resources with locks or semaphores. These techniques help in building high-load systems and real-time data processing pipelines. They are crucial when developing scalable web applications and services that demand robust concurrency management.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio-task.html
- https://realpython.com/python-async-features/
- https://medium.com/@kennethreitz/async-await-in-python-3-5-7b580ca64b73

**Tutorial:**
- Creating Tasks:
    - Use asyncio.create_task to run coroutines concurrently.
```py
import asyncio

async def task_function(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    task1 = asyncio.create_task(task_function("Task 1", 1))
    task2 = asyncio.create_task(task_function("Task 2", 2))
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
```

- Handling Timeouts:
    - Use asyncio.wait_for to set timeouts.
```py
    async def timeout_task():
        await asyncio.sleep(2)
        return "Completed"

    async def main_timeout():
        try:
            result = await asyncio.wait_for(timeout_task(), timeout=1)
        except asyncio.TimeoutError:
            result = "Task timed out"
        print(result)

    asyncio.run(main_timeout())
```
- Explanation: This demonstrates cancelling a task if it exceeds the allotted time.

### Exercise:

- Problem: Write an async function that launches several tasks with a timeout and handles cancellations gracefully.
    -Steps to Solve:
        - Create multiple tasks using create_task.
        - Wrap them with asyncio.wait_for and handle possible timeouts.

### Challenge:

- Problem: Implement an asynchronous rate limiter that allows only a fixed number of tasks per second.
    - Hint: Use an asyncio semaphore to control the concurrency.

## Session 7: Implementing Logging Best Practices in Python

**Goal:**
Learn to integrate and configure logging in Python applications for effective debugging and monitoring.

**Definition:**
Logging captures runtime events, errors, and general application flow. Python’s built-in logging module, along with third-party libraries like loguru, provides flexibility and ease of use. It is essential for debugging, performance monitoring, and security auditing in production systems.

**Documentation Reference:**

- https://docs.python.org/3/library/logging.html
- https://loguru.readthedocs.io/en/stable/
- https://realpython.com/python-logging/

**Tutorial:**
- Basic Logging Setup:
    - Configure the built-in logging module.
```py
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log')
logging.info("This is an info message")
logging.error("This is an error message")
```
- Using loguru:
    - Install and use loguru for a simpler logging experience.
```py
    from loguru import logger

    logger.add("file.log", rotation="1 MB")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.error("Error message")
```
    Explanation: The examples show both native and third-party logging configurations.

### Exercise:

- Problem: Create a Python script that logs messages at DEBUG, INFO, WARNING, and ERROR levels.
    - Steps to Solve:
        - Configure logging using the built-in module.
        - Log messages at different severity levels.

### Challenge:

- Problem: Enhance the logging setup to rotate log files daily and include detailed timestamps.
    - Hint: Use TimedRotatingFileHandler from the logging.handlers module.

## Session 8: Introduction to Testing in Python with pytest

**Goal:**
Learn the basics of writing and running tests using pytest to improve code reliability.

**Definition:**
Testing ensures that code behaves as expected. pytest is a powerful testing framework that simplifies writing tests and offers rich features like fixtures and parametrization. It is used for unit testing, integration tests, and continuous integration pipelines to catch errors early in development.

**Documentation Reference:**

- https://docs.pytest.org/en/stable/getting-started.html
- https://realpython.com/pytest-python-testing/
- https://docs.python.org/3/library/unittest.html

**Tutorial:**

- Create a simple function (e.g., addition).
```py
# app.py
def add(a, b):
    return a + b
```
- Write a test for the function.
```py
# test_app.py
from app import add

def test_add():
    assert add(2, 3) == 5
```

- Run tests using:
```bash
    pytest
```

### Exercise:

- Problem: Write a Python function that multiplies two numbers and create a corresponding pytest test.

### Challenge:

- Problem: Write tests for a recursive factorial function using pytest parametrization.
    - Hint: Use the @pytest.mark.parametrize decorator.

## Session 9: Advanced Testing Strategies in Django using pytest

**Goal:**
Explore comprehensive testing techniques in Django projects using pytest to ensure robust web application functionality.

**Definition:**
Advanced testing in Django involves creating tests for models, views, and API endpoints using pytest-django. This approach leverages fixtures, parametrization, and a dedicated test database. It is essential for verifying that all components of a Django application work together as expected, from data models to user interfaces.

**Documentation Reference:**

- https://pytest-django.readthedocs.io/en/latest/
- https://docs.djangoproject.com/en/3.2/topics/testing/overview/
- https://realpython.com/django-testing-guide/

**Tutorial:**
- Setup:
    - Install pytest-django:
```bash
    pip install pytest-django
```
- Step-by-Step Example:
    - Create a simple Django model.
```py
# models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
```
- Write a test to check model creation.
```py
    # test_models.py
    import pytest
    from myapp.models import Item

    @pytest.mark.django_db
    def test_item_creation():
        item = Item.objects.create(name="Test", value=10)
        assert item.name == "Test"
        assert item.value == 10
```
- Explanation: The test uses the Django test database to create and verify an Item instance.

### Exercise:

- Problem: Create a Django model for a BlogPost and write pytest tests to verify its methods.
    - Steps to Solve:
        - Define the BlogPost model with title, content, and published date.
        - Write tests for creating and retrieving BlogPosts.

### Challenge:

- Problem: Develop a full test suite for a Django REST API endpoint (e.g., listing BlogPosts) using pytest fixtures and parametrization.
    - Hint: Create fixtures for BlogPost objects and test the API response structure.
