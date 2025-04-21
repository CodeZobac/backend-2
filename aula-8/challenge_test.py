import pytest

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

@pytest.mark.parametrize("input,expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
])
def test_factorial(input, expected):
    assert factorial(input) == expected