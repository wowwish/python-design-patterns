# The Adapter design pattern tries to modify/configure/adapt the interface that you are given,
# to the interface that you actually need (similar to an electrical adapter for electrical needs 
# of gadgets).

# An Adapter is a construct which adapts an existing interface X, to conform to the required interface Y.
# Match the API you have to the API you need. The Adapter is a component (class) that aggregates or references
# the Adaptee (the class that needs adaptation to the requirement). When intermediate representations
# pile up, use caching and other optimizations!

class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x

# an API to simulate drawing a point at position (x, y)
def draw_point(p):
    print('.', end="")

# ^^ You are given this as the starting point - use this code to draw rectangles

# Here, we want to represent a Line as a series of Points
# vv implementation built using Adapter pattern

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

# A rectangle represented by a list of lines
class Rectangle(list):
    def __init__(self, x, y, width, height):
        super().__init__() # calling the parent class constructor
        # The four sides of a Rectangle
        self.append(Line(Point(x, y), Point(x + width, y)))
        self.append(Line(Point(x + width, y), Point(x + width, y + height)))
        self.append(Line(Point(x, y), Point(x, y + height)))
        self.append(Line(Point(x, y + height), Point(x + width, y + height)))


# Adapter class - one instance of this is created for each 'Line' instance
class LineToPointAdapter(list):
    # 'count' is the number of Points generated (class variable - only used when no caching)
    count = 0
    def __init__(self, line):
        super().__init__() # invoking the constructor of 'List' (parent class)
        self.count += 1
        print(f'{self.count}: Generating points for line [{line.start.x}, {line.start.y}] -> [{line.end.x}, {line.end.y}]')
        # Get the start, end , top, bottom of the line (line can be slanted, at an angle)
        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = max(line.start.y, line.end.y)
        bottom = min(line.start.y, line.end.y)

        if right - left == 0: # if line is parallel to the y axis
            for y in range(top, bottom):
                self.append(Point(left, y))
        elif line.end.y - line.start.y == 0: # if line is parallel to the x axis
            for x in range(left, right):
                self.append(Point(x, top))

class LineToPointAdapterCached: # Inheritance of the 'list' class is omitted because of caching in dictionary
    cache = {} # To avoid regenerating the same points upon subsequent instaltiation of this class
    # This 'cache' is a dictionary of list of points
    def __init__(self, line):
        super().__init__() # invoking the constructor of 'List' (parent class)
        self.h = hash(line) # calculate a unique hash value for every unique line to be stored in the cache
        if self.h in self.cache:
            return # do nothing if the list of points in the rectangle is already cached
        print(f'Generating points for line [{line.start.x}, {line.start.y}] -> [{line.end.x}, {line.end.y}]')
        # Get the start, end , top, bottom of the line (line can be slanted, at an angle)
        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = max(line.start.y, line.end.y)
        bottom = min(line.start.y, line.end.y)

        points = [] # list of points in the rectangle

        if right - left == 0: # if line is parallel to the y axis
            for y in range(top, bottom):
                points.append(Point(left, y))
        elif line.end.y - line.start.y == 0: # if line is parallel to the x axis
            for x in range(left, right):
                points.append(Point(x, top))

        self.cache[self.h] = points

        # Define the iteration behaviour of an instance of this class since we iterate over it
        # in the 'draw_rectangle' function defined below.
    def __iter__(self):
        # The iter() is used to create an object that will iterate one element at a time.
        # It optionally takes an additional argument called the sentinel element which will
        # terminate the iteration sequence when encountered by the __next__() call on the 
        # object returned by iter()
        return iter(self.cache[self.h])

def draw_rectangle(rcs):
    print('\n\n--- Drawing some stuff ---\n')
    for rc in rcs: # for every 'Rectangle' instance in the 'rcs' list
        for line in rc: # for each line in the list of 'Rectangle' instance
            adapter = LineToPointAdapterCached(line) # Instantiate the Adapter for every 'Line' object
            for p in adapter: # for every point in the adapter (list)
                draw_point(p)


if __name__ == '__main__':
    rcs = [Rectangle(1, 1, 10, 10), Rectangle(3, 3, 6, 6)]
    draw_rectangle(rcs)
    # The Adapter (LineToPointAdapter) actually generates temporary objects
    # This is illustrated by the regeneration of points by the second call to 'draw_rectangle()'
    # using the same lines.
    # Notice that when we are using the Cached version of the Adapter class, we are not re-generating
    # the Points on the second call of 'draw_rectangle()', with the same input arguments.
    draw_rectangle(rcs)
    print()



# EXERCISE

# You are given a class called Square and a function calculate_area() which calculates the area of a given 
# rectangle. In order to use Square in calculate_area, instead of augmenting it with width/height members, 
# please implement the SquareToRectangleAdapter class. This adapter takes a square and adapts it in such a way 
# that it can be used as an argument to calculate_area().


class Square:
    def __init__(self, side=0):
        self.side = side

def calculate_area(rc):
    return rc.width * rc.height

# '@property' decorator is used to set attributes for this Adapter class because by following
# this way, any modifications to the 'side' attribure made to the 'square' object after its instantiation 
# will be reflected in the Adapter class as well
class SquareToRectangleAdapter:
    def __init__(self, square):
        self.square = square
    @property
    def width(self):
        return self.square.side

    @property
    def height(self):
        return self.square.side