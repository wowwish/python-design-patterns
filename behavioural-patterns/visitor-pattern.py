# The Visitor Design Pattern allows adding extra behaviours to entire 
# hierarchies of classes. It is used when you need to define a new
# operation on an entire class hierarchy. For example: make a document 
# model printable to formats like HTML/Markdown.
# We do not want to modify every class in the hierarchy in many cases
# where a new functionality has to be added to all of the classes in the
# hierarchy. 


# The Visitor is a component (class or a collection) that knows how to 
# traverse a data structure composed of (possibly related) types.

# The Visitor Component (Class) will need access to the non-common
# aspects of classes in the hierarchy as well.
# Create an external component to handle rendering. Type checks on the
# underlying root class of the Visitor component will usually be implicit
# (such as with the use of decorators), rather than using explicit checks.

# Consider a Simple addition Expression as an Example:

# THE INTRSIVE (MODIFYING CLASS BEHAVIOUR) VISITOR APPROACH

# Here, the Visitor (the variable 'buffer' in this example) that will jump 
# into classes and modify their behaviour - hence it is "Intrusive". 
# It also goes against the Open-Closed Principle. 
# In this specific case, the Visitor is a list that is passed around across
# different classes and the methods 'print' and 'eval' has to be 
# implemented in all the classes that modify this Visitor component (a list)
# This is NOT GOOD PRACTICE!!


class DoubleExpression:
    def __init__(self, value):
        self.value = value
    def print(self, buffer):
        buffer.append(str(self.value))
    def eval(self):
        return self.value
    
class AdditionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left
    def print(self, buffer):
        buffer.append('(')
        self.left.print(buffer)
        buffer.append('+')
        self.right.print(buffer)
        buffer.append(')')
    def eval(self):
        return self.left.eval() + self.right.eval()

    

# if __name__ == '__main__':
#     # 1 + (2 + 3)
#     e = AdditionExpression(DoubleExpression(1), AdditionExpression(DoubleExpression(2), DoubleExpression(3)))
#     buffer = []
#     e.print(buffer)
#     print(''.join(buffer), ' = ', e.eval())



# A REFLECTIVE (CEHCKING OF TYPE) VISITOR APPROACH

# The Reflective Visitor uses Type Checks on instancess (check the class
# of instances) and uses that to implement additional functionality to
# the instances. Note that here, the Visitor Component is implemented
# as a seperate class called 'ExpressionPrinter'

# The Reflective Visitor has one downside: whenever a new type of class
# is added to the hierarchy, the Reflexive Visitor's functionalities need
# to be modified to account for this new type of class (if a new class
# called 'SubtractionExpression' is added here, we need to take care of
# the instances of this type in 'ExpressionPrinter.print()' static method)

from abc import ABC # For creating abstract classes

# An Interface to the Visitor's 'print' method
# Such Interfaces will be imbued with APIs to the additional functionalities
# implemented in the Visitor
class Expression(ABC):
    pass

class DoubleExpression(Expression):
    # Note that we inherit the Interface with an API to the Visitor's
    # ('ExpressionPrinter') new Functionality
    def __init__(self, value):
        self.value = value

# The Reflective Visitor Class
class ExpressionPrinter:
    @staticmethod
    def print(e, buffer): # This is a class method
        if isinstance(e, DoubleExpression):
            buffer.append(str(e.value))
        elif isinstance(e, AdditionExpression):
            buffer.append('(')
            ExpressionPrinter.print(e.left, buffer) # recursion
            buffer.append('+')
            ExpressionPrinter.print(e.right, buffer) # recursion
            buffer.append(')') 

# Imbue the Interface with the Visitor's new functionality and inherit
# this interface in the classes without modifying their underlying code!
Expression.print = lambda self, b: ExpressionPrinter.print(self, b)

class AdditionExpression(Expression):
    # Note that we inherit the Interface with an API to the Visitor's
    # ('ExpressionPrinter') new Functionality
    def __init__(self, left, right):
        self.right = right
        self.left = left

# if __name__ == '__main__':
#     # '1 + (2 + 3)' will be abstracted as a recursive data structure
#     e = AdditionExpression(DoubleExpression(1), AdditionExpression(DoubleExpression(2), DoubleExpression(3)))
#     buffer = []
#     e.print(buffer)
#     print()
#     # Using the class method of 'ExpressionPrinter'
#     ExpressionPrinter.print(e, buffer)
#     print(''.join(buffer))



# THE CLASSIC (DOUBLE DISPATCH) VISITOR APPROACH

# The DOUBLE DISPATCH name originates from the fact that the control flow in this approach goes from
# an accept() method to a visit() method implementation. This approach is not required in Python
# due to its duck-typing feature (dynamic typing).
# In this approach, we use a visit() method that is decorated by 'visitor' which checks for appropriate
# class type and allocates the correct overloaded 'visit()' method to the instance. Then, when you call
# the 'visit()' method, the entire heirarchy of classes/instances get's traversed!

# This approach can be made completely un-intrusive by adding the 
# 'accept()' method to the classes by way of inheriting an Interface that
# implements it, just like in the case of the previous Reflective Visitor
# example!



# This is a piece of Infrastructural Code that makes sure that the overloaded 'view()' methods
# in the Visitor 'ExpressionPrinter' are called according to the respective 
# instance types.
# 'view(self, ae)' for 'AdditionExpression' and 'view(self, de)' for 'DoubleExpression' types)
# taken from https://tavianator.com/the-visitor-pattern-in-python/
# The trick here is that the decorator replaces all the visit methods with '_visitor_impl' (redefining 
# an existing method is fine in Python). But before it does that, it stores the original method in a 
# dictionary, '_methods', keyed by the visitor class and the desired argument type. Then, when visit 
# is invoked, '_visitor_impl' looks up the appropriate implementation and invokes it based on the 
# argument type.


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    # returns __main__.<class_name>
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')] # Extract the class name from the object / instance


# Stores the actual visitor methods for corresponding Visitor type and argument type of 'visit()' method
_methods = {} # Dictionary where the key is a tuple pair of the class name of the Visitor 
# ('ExpressionPrinter' or 'ExpressionEvaluator') and the type of the object/instance which is to
# be visited by the visitor ('DoubleExpression' or 'AdditionExpression').


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg) # calls the corresponding overloaded version of 'visit()' from
    # the appropriate Visitor class.

# The actual @visitor decorator that takes as argument, the type of the object/instance to be visited
# ('AdditionExpression' or 'DoubleExpression')
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator


# ↑↑↑ LIBRARY CODE ↑↑↑




class DoubleExpression:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor): # double-dispatch
        visitor.visit(self)


class AdditionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left
    def accept(self, visitor): # double-dispatch
        visitor.visit(self)


class SubtractionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left
    def accept(self, visitor): # double-dispatch
        visitor.visit(self)


class ExpressionPrinter:
    def __init__(self):
        self.buffer = []
    def __str__(self):
        return ''.join(self.buffer)
    # We apply function overloading on this 'visit()' method which is
    # the crucial method of the Classic Visitor implementation!
    @visitor(DoubleExpression)
    def visit(self, de): # For 'DoubleExpression' instances
        self.buffer.append(str(de.value))
    @visitor(AdditionExpression)
    def visit(self, ae): # For 'AdditionExpression' instances
        self.buffer.append('(')
        # self.visit(ae.left)
        ae.left.accept(self) # double-dispatch is used here, but visit() can be called directly due to
        # duck-typing in python
        self.buffer.append('+')
        # self.visit(ae.right)
        ae.right.accept(self) # double-dispatch is used here, but visit() can be called directly due to
        # duck-typing in python
        self.buffer.append(')')

# Another Visitor Class
class ExpressionEvaluator:
    def __init__(self):
        self.value = None
    @visitor(DoubleExpression)
    def visit(self, de):
        self.value = de.value
    @visitor(AdditionExpression)
    def visit(self, ae):
        self.visit(ae.left)
        temp = self.value # cache the value after visiting part of the expression (stateful Visitor)
        self.visit(ae.right)
        self.value += temp

if __name__ == '__main__':
    # '1 + (2 + 3)' will be abstracted as a recursive data structure
    e = AdditionExpression(DoubleExpression(1), SubtractionExpression(DoubleExpression(2), DoubleExpression(3)))
    printer = ExpressionPrinter()
    printer.visit(e)
    evaluator = ExpressionEvaluator()
    evaluator.visit(e)
    print(f'{printer} = {evaluator.value}')





# EXERCISE


# You are asked to implement a visitor called 'ExpressionPrinter' for printing different mathematical 
# expressions. The range of expressions covers addition and multiplication - please put round brackets 
# around addition operations (but not multiplication ones)! Also, please avoid any blank spaces in 
# output.
# Example:
#   - Input: AdditionExpression(Value(2), Value(3)) 
#   - Output: (2+3) 


# taken from https://tavianator.com/the-visitor-pattern-in-python/

from abc import ABC


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    key = (_qualname(type(self)), type(arg))
    if not key in _methods:
        raise Exception('Key % not found' % key)
    method = _methods[key]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator

# ↑↑↑ LIBRARY CODE ↑↑↑

class Value:
    def __init__(self, value):
        self.value = value


class AdditionExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left


class MultiplicationExpression:
    def __init__(self, left, right):
        self.right = right
        self.left = left


class ExpressionPrinter:
    def __init__(self):
        self.buffer = []
    @visitor(AdditionExpression)
    def visit(self, ae):
        self.buffer.append('(')
        self.visit(ae.left)
        self.buffer.append('+')
        self.visit(ae.right)
        self.buffer.append(')')
    @visitor(MultiplicationExpression)
    def visit(self, me):
        self.visit(me.left)
        self.buffer.append('*')
        self.visit(me.right)
    @visitor(Value)
    def visit(self, v):
        self.buffer.append(str(v.value))

    def __str__(self):
        return ''.join(self.buffer)