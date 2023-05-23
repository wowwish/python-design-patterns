# LISKOV SUBSTITUTION PRINCIPLE

# The Liskov Substitution Principle states that whenever you have an interface (the use_it() function
# in this case) taking some sort of Base class (Rectangle), You should be able to use the methods of
# the Base class on any of its Sub classes (Inheriting classes) without changing the behaviour.
# Objects of the Subclass should behave the same way and must be replaceable with objects of the Superclass

class Rectangle:
    def __init__(self, width, height):
        # the attributes 'height' and 'width' are non-public attributes (ther apre prefixed with '_')
        # to indicate that they should not be accessed using the '.' operator.
        self._height = height
        self._width = width
    # Properties represent an intermediate functionality between a plain attribute (or field) and a method. 
    # In other words, they allow you to create methods that behave like attributes. 
    # With properties, you can change how you compute the target attribute whenever you need to do so.
    # The underlying method will allow you to modify their internal implementation and perform actions on 
    # them right before your users access and mutate them.
    # The main advantage of Python properties is that they allow you to expose your attributes as part of your 
    # public API. If you ever need to change the underlying implementation, then you can turn the attribute into 
    # a property at any time without much pain. 

    # Python’s property() is the Pythonic way to avoid formal getter and setter methods in your code. 
    # This function allows you to turn class attributes into properties or managed attributes. 
    # Since property() is a built-in function, you can use it without importing anything. Additionally, 
    # property() was implemented in C to ensure optimal performance.

    # The @property decorator must decorate the getter method.
    # The docstring must go in the getter method
    # The setter and deleter methods must be decorated with the name of the getter method plus 
    # '.setter' and '.deleter', respectively.
    @property
    def area(self):
        return self._width * self._height
    def __str__(self):
        return f'Width: {self.width}, Height: {self.height}'
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    

class Square(Rectangle):
    def __init__(self, size):
        Rectangle.__init__(self, size, size)
        # Whatever happens, the square should satisfy height == width
        # UNFORTUNATELY, THIS BREAKS THE LISKOV SUBSTITUTION PRINCIPLE!
        # THE SETTERS BELOW VIOLATE THE LISKOV SUBSTITUTION PRINCIPLE!
    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value
    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value

# function to check if the expected area matches the calculated area
# This function holds true only for the Rectangle class and does not work
# on any other classes that derive from the Rectangle class.
def use_it(rc):
    w = rc.width
    print(rc.width, rc.height)
    # We set the height here, which also affects the width of the square. The line below breaks the
    # Liskov Substitution Principle because, while we expect 'width' to remain unchanged in
    # an instance of base class 'Rectangle', it is modified in an instance of the subclass 'Square'
    rc.height = 10
    expected = int(w * 10)
    print(rc.width, rc.height)
    print(f'Expected an area of {expected}, got {rc.area}')

rc = Rectangle(2, 3)
use_it(rc)

sq = Square(5)
use_it(sq)

# TO FIX THIS ISSUE, PERHAPS THE SQUARE SHOULD BE A SEPERATE CLASS BY ITSELF THAT DOES NOT INHERIT
# FROM RECTANGLE.