"""
Factory Pattern Implementation for Shape Objects

This module demonstrates the Factory design pattern to create different shape objects.
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self):
        """Draw the shape."""
        pass
    
    @abstractmethod
    def calculate_area(self):
        """Calculate the area of the shape."""
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def draw(self):
        return f"Drawing a circle with radius {self.radius}"
    
    def calculate_area(self):
        return 3.14159 * self.radius * self.radius


class Square(Shape):
    def __init__(self, side_length):
        self.side_length = side_length
    
    def draw(self):
        return f"Drawing a square with side length {self.side_length}"
    
    def calculate_area(self):
        return self.side_length * self.side_length


def shape_factory(shape_type, **kwargs):
    shapes = {
        'circle': Circle,
        'square': Square
    }
    
    if shape_type.lower() not in shapes:
        raise ValueError(f"Shape type '{shape_type}' not supported. Available types: {', '.join(shapes.keys())}")
    
    return shapes[shape_type.lower()](**kwargs)


# Example usage
if __name__ == "__main__":
    # Create a circle with radius 5
    circle = shape_factory('circle', radius=5)
    print(circle.draw())
    print(f"Circle area: {circle.calculate_area()}")
    
    # Create a square with side length 4
    square = shape_factory('square', side_length=4)
    print(square.draw())
    print(f"Square area: {square.calculate_area()}")