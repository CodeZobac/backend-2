# Tests for the calculator module
import pytest
from calculator import add, subtract, multiply, divide, power


class TestCalculator:
    """Test class for calculator functions."""
    
    def test_add(self):
        """Test addition function."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
        assert add(1.5, 2.5) == 4.0
    
    def test_subtract(self):
        """Test subtraction function."""
        assert subtract(5, 3) == 2
        assert subtract(0, 0) == 0
        assert subtract(-1, -1) == 0
        assert subtract(10.5, 5.5) == 5.0
    
    def test_multiply(self):
        """Test multiplication function."""
        assert multiply(3, 4) == 12
        assert multiply(0, 5) == 0
        assert multiply(-2, 3) == -6
        assert multiply(2.5, 4) == 10.0
    
    def test_divide(self):
        """Test division function."""
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
        assert divide(-8, 4) == -2
        assert divide(0, 5) == 0
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_power(self):
        """Test power function."""
        assert power(2, 3) == 8
        assert power(5, 0) == 1
        assert power(4, 0.5) == 2.0
        assert power(-2, 2) == 4


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10.5, 2.5, 13.0),
])
def test_add_parametrized(a, b, expected):
    """Parametrized test for addition."""
    assert add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (15, 3, 5),
    (100, 4, 25),
    (1, 1, 1),
])
def test_divide_parametrized(a, b, expected):
    """Parametrized test for division."""
    assert divide(a, b) == expected
