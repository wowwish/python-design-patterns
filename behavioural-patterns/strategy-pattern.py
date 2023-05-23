# In the Strategy Design Pattern, the system behaviour is partially specified at runtime.
# Many algorithms can be decomposed into their High-level (general) and Low-level 
# (object / system specific) parts.
# For example, making tea can be decomposed into:
#   * High-level description: boil water, pour into cup etc. to make a hot beverage
#   * Low-level description: tea-specific things like putting the tea bag into boiled water, let 
#     it simmer, pull the tea bag out when the tea is the right colour etc.
# The Strategy Design Pattern is all about decomposing these two parts of the algorithm.
# The High-level algorithm can be reused for other purposes. In this example, we can use the High-level
# algorithm to create either coffee or hot chocolate. The Low-level parts for these use cases can be
# specified by different beverage-specific Strategies and can be put into the High-level part for
# creating a beverage-specific Strategy.

# The Strategy Design Pattern enables the exact behaviour of a system (object) to be selected 
# at runtime.

# Essentially in the Strategy Pattern, you define an algorithm at a high-level and define an 
# Interface that you expand for each Strategy (low-level implementation with details) to follow.
# The Strategies create will provide for dynamic composition in the resulting object.


# As an example, consider a text processor that can process different element types and output them to
# one of two possible formats (HTML or Markdown):

from abc import ABC # For creating Abstract Base Classes
from enum import Enum, auto # For creating Enumerator classes and auto-assigning the index for 
# the Enumerator elements

# A bluprint for implementing text processor Strategies
class ListStrategy(ABC):
    def start(self, buffer): pass # take care of starting tag for the list of text in the buffer (if required)
    def end(self, buffer): pass # take care of ending tag for the list of text in the buffer (if required)
    def add_list_item(self, buffer, item): pass # add an item to the buffer after processing it appropriately

# A Strategy for creating Markdown list from a list of input text
class MarkdownListStrategy(ListStrategy):
    def add_list_item(self, buffer, item):
        buffer.append(f'  * {item}\n')

# A Strategy for creating HTML (unordered list) from a list of input text
class HtmlListStrategy(ListStrategy):
    def start(self, buffer):
        buffer.append('<ul>\n')
    def add_list_item(self, buffer, item):
        buffer.append(f'  <li>{item}</li>\n')
    def end(self, buffer):
        buffer.append('</ul>\n')


class OutFormat(Enum):
    MARKDOWN = auto()
    HTML = auto()


class TextProcessor:
    def __init__(self, list_strategy=HtmlListStrategy()):
        self.list_strategy = list_strategy
        self.buffer = [] # the buffer list that contains the text to process (words)
    def append_list(self, items):
        ls = self.list_strategy
        ls.start(self.buffer)
        for item in items:
            ls.add_list_item(self.buffer, item)
        ls.end(self.buffer)
    
    def set_output_format(self, format):
        if format == OutFormat.MARKDOWN:
            self.list_strategy = MarkdownListStrategy()
        elif format == OutFormat.HTML:
            self.list_strategy = HtmlListStrategy()

    def clear(self):
        self.buffer.clear()
    
    def __str__(self):
        return ''.join(self.buffer)
    

if __name__ == '__main__':
    items = ['foo', 'bar', 'baz']
    
    tp = TextProcessor()
    tp.set_output_format(OutFormat.MARKDOWN)
    tp.append_list(items)
    print(tp)

    tp.set_output_format(OutFormat.HTML)
    tp.clear()
    tp.append_list(items)
    print(tp)





# EXERCISE

# Consider the quadratic equation and its canonical solution:

#   ax^2 + bx + c = 0
#   x = (-b +/- sqrt(b^2 - 4ac)) / 2a

# The part b^2-4*a*c is called the discriminant. Suppose we want to provide an API with two different 
# strategies for calculating the discriminant:
# In 'OrdinaryDiscriminantStrategy', If the discriminant is negative, we return it as-is. This is OK, 
# since our main API returns Complex numbers anyway.
# In 'RealDiscriminantStrategy', if the discriminant is negative, the return value is NaN (not a number). NaN propagates throughout the calculation, so the equation solver gives two NaN values. In Python, you make such a number with float('nan').

# Please implement both of these strategies as well as the equation solver itself. With regards to 
# plus-minus in the formula, please return the + result as the first element and - as the second. 
# Note that the solve() method is expected to return complex values.


import math # For passing downstream unit tests
import cmath # For creating and processing Complex numbers

class DiscriminantStrategy(ABC):
    def calculate_discriminant(self, a, b, c):
        pass


class OrdinaryDiscriminantStrategy(DiscriminantStrategy):
    def calculate_discriminant(self, a, b, c):
        return (b * b) - (4 * a * c)


class RealDiscriminantStrategy(DiscriminantStrategy):
    def calculate_discriminant(self, a, b, c):
        discriminant = (b * b) - (4 * a * c)
        if discriminant < 0:
            return float('nan')
        return discriminant


class QuadraticEquationSolver:
    def __init__(self, strategy):
        self.strategy = strategy

    def solve(self, a, b, c):
        """ Returns a pair of complex (!) values """
        discriminant = complex(self.strategy.calculate_discriminant(a, b, c), 0)
        val1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
        val2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
        return (val1, val2)