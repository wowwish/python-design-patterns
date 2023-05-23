# Open-Closed Principle - Open for Extension, but Closed for Modification
# After you have written and tested a Class, you should not modify it. Instead, Extemd it.

# Assume that you own a website that sells products. The products will have their own classes with properties
# like color, size etc.

# An enumeration is a set of symbolic names (members) bound to unique values
from enum import Enum

# The enum members have names and values (the name of Color.RED is RED, the value of Color.BLUE is 3, etc.)
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

# Now let's assume that one of the requirements in your application is to filter the products by color.

class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            # The yield statement produces a generator object and can return multiple values to the caller 
            # without terminating the program
            if p.color == color: yield p # makes this function return a generator
    # Now, your manager asks you to add filtering by size functionality
    def filter_by_size(Self, products, size):
        for p in products:
            if p.size == size: yield p # makes this function return a generator
    # THIS VIOLATES THE OPEN-CLOSED PRINCIPLE! 
    # THIS GAME OF ADDING ADDITIONAL FILTER FUNCTIONALITY CAN GO ON FOREVER AND CAN LEAD TO UNPLEASANT RESULTS.
    # For example, if your manager again comes back and askes for filtering by both color and size:
    def filter_by_color_and_size(self, products, color, size):
        for p in products:
            if p.color == color and p.size == size:
                yield p # makes this function return a generator
    def filter_by_color_or_size(self, products, color, size):
        pass
    # IN ADDITION TO BREAKING THE OPEN-CLOSED PRINCIPLE, THIS ALSO CAUSES WHAT IS CALLED A STATE-SPACE EXPLOSION:
    # Just two criteria for filtering leads to the creation of three or more methods. This does not scale
    # well! If you have three such filtering criteria, you will have atleast seven different methods to 
    # implement (STATE-SPACE EXPLOSION!)

    # TO SOLVE THIS ISSUE, WE CAN IMPLEMENT AN ENTERPRISE LEVEL PATTERN CALLED - SPECIFICATION!
    # A SPECIFICATION PATTERN INVOLVES TWO CLASSES TO PERFORM THE FILTERING FUNCTIONALITY:

# Class to determine whether a particular item satisfies a particular criteria
class Specification: # Base Class that will be inherited and extended
    def is_satisfied(self, item):
        pass
    # We can also overlaod the '&' operator in python to make it combine multiple Specification instances!
    def __and__(self, other):
        return AndSpecification(self, other)


class Filter: # Base class that will be inherited and extended with the filtering criterion logic
    def filter(self, items, spec): # 'spec' here is a filtering specification that relates to
    # the Specification class above!
        pass

# Now, suppose you want to filter by color:
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color
    def is_satisfied(self, item):
        return item.color == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size
    def is_satisfied(self, item):
        return item.size == self.size
    
# We can also build COMBINATOR SPECIFICATION CLASSES
class AndSpecification(Specification):
    # This specification can take up variable number of filter criterion
    # An item should satisfy every single one of those criterion
    def __init__(self, *args): # constructor takes up variable number of arguments (Specification instances)
        self.args = args
    def is_satisfied(self, item):
        # Map every specification passed in and check if every one of them is satisfied by the item
        return all(map(lambda spec: spec.is_satisfied(item), self.args))
    
class BetterFilter(Filter):
    # This method is not included in the Filter Base Class because this allows for flexibility in the
    # logic of filtering. Also, we follow the open-closed principle and extend the base class instead of
    # modifying the base class directly.
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item # makes this function return a generator

if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    # OLD APPROACH OF FILTERING THAT BREAKS THE OPEN-CLOSED PRINCIPLE
    pf = ProductFilter()
    print('Green products (old):')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f'    - {p.name} is green')

    # NEW AND BETTER APPROACH THAT STICKS TO THE OPEN-CLOSED PRINCIPLE
    bf = BetterFilter()
    print('Green products (new):')
    green = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green):
        print(f'    - {p.name} is green')
    
    # Finding all the large products
    print('Large products:')
    large = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large):
        print(f'    - {p.name} is large')

    print('large blue items:')
    # large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))
    large_blue = large & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue):
        print(f'    - {p.name} is large and blue')
