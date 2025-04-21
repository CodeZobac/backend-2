

def multiply(a, b):
    return a * b

if __name__ == "__main__":
    import pytest

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 6),
        (0, 5, 0),
        (-1, 8, -8),
        (7, 7, 49),
    ])
    def test_multiply(a, b, expected):
        assert multiply(a, b) == expected

    pytest.main()