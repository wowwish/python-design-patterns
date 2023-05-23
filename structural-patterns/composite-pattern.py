# The goal of the Composite Design Pattern is to treat individual components (single classes or scalars) and
# group of objects (aggregates of components) in an uniform fashion.
# It is used to treat both individual Classes (scalars) and Compound Classes (or Inheritance based
# Class Hierarchies) in the same way.

# One object uses the properties/members of another object through either Inheritance or Composition.
# Composition lets us make "Compound objects" such as a mathematical expression composed of simple
# expressions; or a grouping of shapes that consists of several shapes.

# In the Composite pattern, an object of class 'Foo' and a object of class 'Sequence' (that yields several
# instances of the class 'Foo') have common API. Some Composed and Singular objects need similar/identical
# behaviours (Treat a Group of objects (Collection) using the exactly same Interface of a Single object 
# (Singular/Scalar)).

# The composite pattern uses recursive data structures to treat single objects and groups of objects
# as the same entity (uniform treatment in both cases).

# Python supports Iteration (for Composites/Collections) with the '__iter__()' method and the 'Iterable'
# abstract class (built-in abstract base class) from the 'collections.abc' package. 
# (from collections.abc import Iterable) This 'Iterable' abstract base class can be used as a guide 
# to specifically require the implementation of the '__iter__()' method.
# A Single object (Scalar) can make itself iterable (or masquerade as a Collection) by 
# yielding 'self' from its '__iter__()' method

# A COLLECTION CLASS CAN ACT AS AN INDIVIDUAL CLASS (SCALAR)


# As an example, think of a drawing app where you can group several geometric shapes together and then drag
# and drop the group like a single shape.

# The recursive Composite component can contain multiple instances of itself as well. So a 'GraphicObject'
# instance can also contain multiple other 'GraphicObject' instances as its individual shape elements
from collections.abc import Iterable  # For creating iterable classes
from abc import ABC  # For creating abstract class


class GraphicObject:
    def __init__(self, color=None):
        self.color = color
        self.children = []  # container for individual shape components
        self._name = 'Group'  # the group name

    @property
    def name(self):
        return self._name

    # utility method for string representation of an instance of this class
    # It creates an unordered list of unordered sub-lists, along with the depth information encoded with
    # the number of '*' characters before the color and name of the shape.
    def _print(self, items, depth):
        items.append('*' * depth)
        if self.color:
            items.append(self.color)
        # Notice the newline character added here to
        items.append(f'{self.name}\n')
        for child in self.children:  # recursively call the _print() method on the children of the
            # current child of this 'Graphbject' instance.
            child._print(items, depth + 1)

    def __str__(self):
        items = []
        # Using the helper method, build an array of strings to be printed that contains the depth
        # and parent-child relationships between the sub-groups of shapes within a grouped graph object.
        self._print(items, 0)
        return ''.join(items)  # convert the array as a single string


class Circle(GraphicObject):
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
    def name(self):
        return 'Circle'


class Square(GraphicObject):
    @property
    def name(self):
        return 'Square'


if __name__ == '__main__':
    drawing = GraphicObject()
    # Just for illustration purposes, we are modifying a read-only attribute of the 'GraphObject' instance!
    # It is a bad coding practive to modify the attributes of an object/class that begin with '_'. Such
    # attributes are supposed to be read-only.
    drawing._name = 'My Drawing'
    drawing.children.append(Square('Red'))
    drawing.children.append(Circle('Yellow'))
    # The recursive 'GraphicObject' instance can  contain multiple instances of 'GraphicObject' as its children
    group = GraphicObject()
    group.children.append(Circle('Blue'))
    group.children.append(Square('Blue'))
    # Here, we are applying the Composite design pattern. The 'GrpahicObject'
    drawing.children.append(group)
    # instance 'group' gets to pretend to be a "scalar" (individual class with no children) shape class like
    # 'Circle' or 'Square'. Here, the 'group' instance is a collection of elements that acts as a single class!
    # invoke the __str__() method of the 'GraphicObject' instance
    print(drawing)


# A SCALAR CLASS (INDIVIDUAL) CAN ALSO ACT AS A COLLECTION CLASS


# As an example, consider Neural Networks.

# An abstract class for a Connector that obeys the Composite design pattern
# A 'Connectable' instance can connect to another instance of the same class, or a collection of instances
# of this class!

class Connectable(Iterable, ABC):
    def connect_to(self, other):
        if self == other:  # A neuron layer cannot connect to itself!
            return
        for s in self:
            for o in other:
                s.outputs.append(o)
                o.inputs.append(s)


# A scalar (individual) class
class Neuron(Connectable):
    def __init__(self, name):
        self.name = name
        self.inputs = []  # connections from the previous layer of neurons
        self.outputs = []  # connections to the next layer of neurons

    # overriding the __iter__() method to define the iteration behaviour of a 'Neuron' instance
    # This method has to be implemented to allow looping over (once) the single element of an instance
    # of this "scalar" class! This allows to implement the Composite pattern where a "scalar" class instance
    # behaves as a collection!
    def __iter__(self):
        # turn a "scalar" (individual) class into a collection class with one element!
        yield self

    def __str__(self):
        return f'{self.name}, ' \
            f'{len(self.inputs)} inputs, ' \
            f'{len(self.outputs)} outputs'

    # def connect_to(self, other):
        # make two-way connections between self and the other neurons
        # self.outputs.append(other)
        # other.inputs.append(self)


# A collection class
class NeuronLayer(list, Connectable):
    def __init__(self, name, count):
        super().__init__()
        self.name = name
        for x in range(0, count):
            # Add 'Neuron' instances with corresponding names to the layer (Remember, this class inherits from
            # the 'list' class and hence can hold multiple values in 'self')
            self.append(Neuron(f'{name}-{x}'))

    def __str__(self):
        return f'{self.name} with {len(self)} neurons'


if __name__ == '__main__':
    neuron1 = Neuron('n1')
    neuron2 = Neuron('n2')
    layer1 = NeuronLayer('L1', 3)
    layer2 = NeuronLayer('L2', 4)
    neuron1.connect_to(neuron2)
    neuron1.connect_to(layer1)
    layer1.connect_to(neuron2)
    layer1.connect_to(layer2)

    print(neuron1)
    print(neuron2)
    print(layer1)
    print(layer2)




# EXERCISE 

# Consider the code presented below. We have two classes called 'SingleValue' and 'ManyValues'. 'SingleValue' 
# stores just one numeric value, but 'ManyValues' can store either numeric values or 'SingleValue' objects.
# You are asked to give both 'SingleValue' and 'ManyValues' a property member called 'sum' that returns a sum of 
# all the values that the object contains. Please ensure that there is only a single method that realizes the 
# property 'sum', not multiple methods.

# Here is a sample unit test:

# import unittest
# class FirstTestSuite(unittest.TestCase):
#     def test(self):
#         single_value = SingleValue(11)
#         other_values = ManyValues()
#         other_values.append(22)
#         other_values.append(33)
        # make a list of all values
        # all_values = ManyValues()
        # all_values.append(single_value)
        # all_values.append(other_values)
        # self.assertEqual(all_values.sum, 66)



class SingleValue:
    def __init__(self, value):
        self.value = value
    @property
    def sum(self):
        return self.value
    def __iter__(self):
        yield self.value

class ManyValues(list):
    def __init__(self):
        super().__init__()
    @property
    def sum(self):
        total = 0
        for item in self:
            if isinstance(item, int):
                total += item
            else:
                total += item.sum
        return total