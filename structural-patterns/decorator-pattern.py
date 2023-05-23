# The Decorator Pattern adds additional behaviour to a class without altering the class itself, without 
# inheriting from the class, through a Decorator implementation that simply references the decorated object. 
# It augments an object with additional functionality.

# The Decorator Pattern forces the implementation of the Open-Closed Principle, as we do not want to 
# rewrite or alter existing code!
# The Decorator Pattern should keep the new functionality as a seperate component/class in order to adhere 
# to the Single Responsibility Principle.
# The pattern also requires the ability to interact with the object implementing this pattern.
# The Decorator simply references the decorated object(s)

# A Decorator keeps the reference to the decorated object(s). It adds utility attributes and methods to
# augment the object's features (without modifying the underlying object). 
# You may or may not forward the calls to the Decorator to its underlying object. You can provide access to 
# the methods and attributes of the underlying object through the Decorator (Proxying). Proxying underlying
# calls can be done dynamically

# Python has many in-built functional form of decorators. These functional form of pythonic decorators

# A FUNCTIONAL DECORATOR (NOT THE TYPICAL DECORATOR DESIGN PATTERN) - Adds additional functionality 
# to a function, and is different from the class-based Decorator Pattern mentioned in the Gang of Four book on
# Design Patterns

import time

# A function Decorator - adds additional functionality of calculating the execution time of an existing function
def time_it(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f'{func.__name__} took {int((end - start) * 1000)}ms')
        return result
    return wrapper # 'time_it' is a function decorator - A function that returns another function

# We can use special syntax in python to apply a decorator to a function. With this syntax, whenever the
# function is called, the function Decorator is applied on it and only the decorated function is invoked.
@time_it
def some_op():
    print('Starting op')
    time.sleep(1) # sleep for 1 sec
    print('We are done')
    return 123

# if __name__ == '__main__':
#     some_op()
    # using the function decorator and calling the returned function using direct syntax
    # time_it(some_op)() 




# A CLASS DECORATOR (ACTUAL DECORATOR PATTERN MENTIONED IN THE BOOK BY THE GANG OF FOUR) - A class that 
# augments a functionality of an existing class

from abc import ABC # for creating abstract classes

class Shape(ABC):
    def __str__(self):
        return ''
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    # The Decorator has to be designed to provide access to methods and attributes of its underlying
    # object like this 'resize' method
    def resize(self, factor):
        self.radius *= factor
    def __str__(self):
        return f'A Circle of radius {self.radius}'
    
class Square(Shape):
    def __init__(self, side):
        self.side = side
    def __str__(self):
        return f'A Square with side {self.side}'
    

# A Decorator Class - Notice that it inherits the 'Shape' class as base to work with the children of 'Shape',
# ie, both the 'Square' and the 'Circle' classes
class ColoredShape(Shape):
    def __init__(self, shape, color):
        # Handling nested decorations of an instance
        if (isinstance(shape, ColoredShape)):
            raise Exception('Cannot apply same decorator twice!')
        # Using a reference of an object of the to class to be decorated instead of inheriting the class to 
        # be decorated directly. The open-closed principle is still intact here.
        self.shape = shape 
        self.color = color
    def __str__(self):
        # Here, 'self.shape' within the f-string corresponds to the string returned by '__str__()' call of 
        # the 'Shape' instance
        return f'{self.shape} has the color {self.color}'

# Another Decorator class
class TransparentShape(Shape):
    def __init__(self, shape, transparency):
        self.shape = shape
        self.transparency = transparency
    def __str__(self):
        # Here, 'self.shape' within the f-string corresponds to the string returned by '__str__()' call of 
        # the 'Shape' instance
        return f'{self.shape} has {self.transparency * 100.0}% transparency'


if __name__ == '__main__':
    circle = Circle(2)
    print(circle)
    # Open-Closed principle implemented in 'ColoredShape' through inheritance
    red_circle = ColoredShape(circle, 'Red')
    print(red_circle)
    # The 'ColoredShape' Decorator does not provide access to methods of the underlying object. This is because
    # of Decorators donot directly inherit the class of the underlying object(s) 
    # red_circle.resize(2) 
    red_half_transparent_circle = TransparentShape(red_circle, 0.5)
    print(red_half_transparent_circle)
    # One downside to this approach is that nothing prevents you from applying the same Decorator twice or
    # more times on a class! This has to be handled in the Decorator class implementation!
    # NOTE: In case of nested application of multiple Decorators, It is difficult to catch the different 
    # error cases due to multiple error situations that grow exponentially with the number of Decorators. 
    # For Example: ColoredShape(TransparentShape(ColoredShape(Square(3), 'Red'), 0.5), 'Green')
    mixed = ColoredShape(ColoredShape(Square(3), 'Red'), 'Green')
    print(mixed)




# DYNAMIC DECORATORS - Decorators with APIs that allow access to the methods and attributes of the underlying
# object. Here, we do not create a high level API in the Decorator class for every method of the underlying
# object. Instead, we use dunder methods like __getattr__() and __setattr__() to dynamically provide access
# to the underlying object's attributes/methods and modify them!

class FileWithLogging:
    def __init__(self, file):
        # The 'file' attribute here corresponds to a opened file handler
        self.file = file
    
    def writelines(self, strings):
        # using the in-built writelines() method of a file-handler object in python
        self.file.writelines(strings)
        print(f'wrote {len(strings)} lines')
    
    # A dynamic Decorator creates proxies for access to attributes and methods of its 
    # underlying object like so: 
    # Override the '__getattr__()', '__setattr__()' and '__delattr__()' methods of the Decorator class to 
    # provide access to the underlying object's attributes and methods

    def __getattr__(self, item):
        # __getattr__(self, name) is an object method that is called if the object's properties are not found. 
        # This method should return the property value or throw AttributeError. 
        # Note that if the object property can be found through the normal mechanism, it will not be called.
        # use getattr(object, name[, default]) method to get an item in the class dictionary. 
        # The getattr() method returns the value of the named attribute of an object. If not found, it returns 
        # the default value provided to the function. 
        # REMEMBER: Since the introduction of metaclasses in Python3, self.__dict__ refers to a dictionary of 
        # the writable attributes and methods of an instance (object)
        return getattr(self.__dict__['file'], item) # This calls the __getattr__() of the underlying 'file' instance
    def __setattr__(self, key, value):
        # Since the introduction of metaclasses in Python3, self.__dict__ refers to a dictionary of 
        # attributes and methods of an instance
        # When the 'file' attribute of this Decorator class has to be set, we set in directly using
        # the self.__dict__ attributes dictionary of the Decorator class itself
        if (key == 'file'):
            self.__dict__[key] = value
        else:
            # For attributes other than 'file', we use the setattr() method on the underlying object
            # of the decorator (the file instance) to invoke the file instance's __setattr__() method
            # and set allow attribute modification / initialization at the underlying class level in
            # the Decorator.
            # The setattr(object, name, value) function sets the value of the attribute of an object by 
            # internally calling the object's __setattr__() method.
            setattr(self.__dict__['file'], key, value)
    def __delattr__(self, item):
        # The delattr(object, item) function an attribute of the attribute of an object by 
        # internally calling the object's __delattr__() method.
        delattr(self.__dict__['file'], item)

    # Providing access to the underlying file instance's __iter__() and __next__() for iteration of the file
    # instance at the Decorator level (works only when these methods are implemented in the file instance 
    # already). KEEP IN MIND THAT DUNDER METHODS (MAGIC METHODS) LIKE __iter__() AND __next__() ARE NOT 
    # OBTAINED USING THE __getattr__() METHOD OF THE DECORATOR CLASS WHEN THEY ARE USED INTERNALLY 
    # DURING ITERATION!
    def __iter__(self):
        return self.file.__iter__()
    
    def __next__(self):
        return self.file.__next__()
    

if __name__ == '__main__':
    file = FileWithLogging(open('hello.txt', 'w'))
    # calling the version of writelines() method that we defined in our Decorator 'FileWithLogging'
    file.writelines(['hello', 'world'])
    # This will use file.__getattr__(file, 'write') to get the in-built write() method of a file-handler object
    file.write('testing')
    # This will use file.__getattr__(file, 'close') to get the in-built close() method of a file-handler object
    file.close()





# EXERCISE

# You are given two types, 'Circle' and 'Square', and a decorator called 'ColoredShape'.
# The decorator adds the color to the string output for a given shape, just as we did in the lecture.
# There's a trick though: the decorator now has a resize() method that should resize the underlying shape. 
# However, only the Circle has a resize() method; the Square does not — do not add it!
# You are asked to complete the implementation of 'Circle', 'Square' and 'ColoredShape'.

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def resize(self, factor):
        self.radius *= factor

    def __str__(self):
        return 'A circle of radius {}'.format(self.radius)

class Square:
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return 'A square with side {}'.format(self.side)


class ColoredShape:
    def __init__(self, shape, color):
        self.color = color
        self.shape = shape

    def resize(self, factor):
        # if the resize() method is implement in the underlying object, use it
        # otherwise, do nothing
        shape_resize = getattr(self.shape, 'resize', None)
        if shape_resize:
            shape_resize(factor)

    def __str__(self):
        return '{} has the color {}'.format(self.shape, self.color) 