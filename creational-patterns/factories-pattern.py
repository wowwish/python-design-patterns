# FACTORY METHODS AND THE ABSTRACT FACTORY

# This design pattern is used when the object creation logic becomes too convoluted (the initializer or
# constructor becomes too long and sophisticated).
# The initializer (constructor) itself is not very descriptive:
#   * Name is always '__init__()' and hence, we cannot fully understand everything it does
#   * The initializer (constructor) cannot be overloaded (function overloading) with same set of arguments
#   having different names.
#   * The initializer (constructor) can turn into 'optional parameter hell' with default values, argument
#   * interactions with one another, organizing the arguments etc


# The factory pattern deals with 'wholesale' object creation (non-piecewise object creation, unlike the
# Builder pattern) and it outsources this process through several ways:
#   * A seperate method (Factory method - typically a class method)
#   * A seperace Class (Factory class)
#   * A hierarchy of factories with Abstract Factory

# A Factory is a component (any entity) reponsible solely for the wholesale (not piecewise) creation of Objects
# A Factory can be an Object, or a method, or even a lambda in python! A Factory can be external, or reside
# inside the object as an inner class!
# Hierarchies of Factories can be used to create related objects.

# A Factory method is a static method (class method) that creates an object (An instance of any class)
 


# FACTORY METHOD IMPLEMENTATION

from enum import Enum
from math import *  # for sin() and cos() functions

# For every coordinate system, we have to add a new enum member and add another check in the
# class constructor below.
# This breaks the open-closed principle (add new functionality by extension, not modification)!


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point:
    # Initializing a cartesian system point or a polar coordinate point.
    # Here, we have to figure out a way to map the arguments 'a' and 'b' to
    # the coordinates of a point in the system, which is another problem!
    # def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
    #     if system == CoordinateSystem.CARTESIAN:
    #         self.x = a
    #         self.y = b
    #     elif system == CoordinateSystem.POLAR:
    #         self.x = a * cos(b)
    #         self.y = a * sin(b)

    # Instead of an initializer (constructor), we can make Factory methods like this:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'

    # Factory method to create a point in the Cartesian coordinate system
    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)

    # Factory method to create a point in the Polar coordinate system
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))

    # Factory Class Implemented inside the main Class itself!
    # The methods of this Factory class can be accessed using 'Point.PointFactory.new_polar_point()'
    # Note that the methods implemented in this Factory Class inside the main Class are not static
    # methods (not class methods) because they may need to use some of the non-static attributes
    # that will be specific to instances of this version of the 'Point' class after initialization,
    # inside this 'PointFactory' class.
    class PointFactory: # class inside a class becomes an inner class or a nested class
        # We can have multiple inner classes and multi-level inner classes in python
        # although such practices are not widely used
        def new_cartesian_point(self, x, y):
            p = Point()
            p.x = x
            p.y = y
            return p

        def new_polar_point(self, rho, theta):
            return Point(rho * cos(theta), rho * sin(theta))
    # If you need to create a PointFactory instance with non-static attributes, you can create it
    # like so:
    # factory = PointFactory(<args>) and then used its methods like 'Point.factory.new_polar_point()'

# FACTORY (CLASS) IMPLEMENATION

# One problem with such Factory classes is that their presence can sometimes go unnoticed by clients!
# You can also move the 'PointFactory' class below, into the 'Point' class itself (class inside a class)
# and use it from there!


class PointFactory:
    # Factory method to create a point in the Cartesian coordinate system
    @staticmethod
    def new_cartesian_point(x, y):
        p = Point()
        p.x = x
        p.y = y
        return p

    # Factory method to create a point in the Polar coordinate system
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * cos(theta), rho * sin(theta))


# if __name__ == '__main__':
#     p = Point(2, 3)
#     p2 = Point.new_polar_point(1, 2)
#     p2 = Point.PointFactory.new_polar_point(1, 2)
#     print(p, p2)




# ABSTRACT FACTORY HEIRARCHY (ABSTRACT BASE CLASSES)
from abc import ABC # To create abstract base class

# An Abstract Base Class
class HotDrink(ABC):
    # An abstract method (unimplemented method)
    def consume(self):
        pass
# An Abstract Factory Class
class HotDrinkFactory(ABC):
    # An abstract Factory method (unimplemented method) that is supposed to return an Object
    def prepare(self):
        pass

class Tea(HotDrink):
    def consume(self):
        print('This tea is delicious')

class Coffee(HotDrink):
    def consume(self):
        print('This coffee is delicious')


class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Put in tea bag, boil water,',
              f'pour {amount}ml, enjoy!')
        return Tea()
    
class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f'Grind some beans, boil water,',
              f'pour {amount}ml, enjoy!')
        return Coffee()

# A function using the Factory methods corresponding to an user input
def make_drink(type):
    if type == 'tea':
        return TeaFactory().prepare(200)
    elif type == 'coffee':
        return CoffeeFactory().prepare(50)
    else:
        return None


# if __name__ == '__main__':
#     entry = input('What kind of drink would you like? ')
#     drink = make_drink(entry)
#     drink.consume()





# ANOTHER APPROACH IS TO USE A COLLECTION OF FACTORIES

import sys
from enum import auto # auto() automatically assigns the integer values to Enum members starting from 1
current_module = sys.modules[__name__] # Get a reference to the current python module file for getting the
# classes implemented in it

class HotDrinkMachine:
    # An enumerator class holding all the available drinks
    class AvailableDrink(Enum): # Violates the Open-Closed Principle!
        # auto() automatically assigns the integer values to Enum members starting from 1
        COFFEE = auto()
        TEA = auto()
    # Python is dynamically typed (performs duck-typing), so, even if the factory methods implemented
    # above such as 'TeaFactory' and 'CoffeeFactory' donot inherit from the abstract Factory class
    # 'HotDrinkFactory', we can still append their instances to this 'self.factories' collection (list)
    factories = [] # collection of Factory classes
    initialized = False # Is the Factory collection initialized ?
    def __init__(self):
        if not self.initialized:
            for d in self.AvailableDrink:
                name = d.name[0] + d.name[1:].lower()
                # Factory class name
                factory_name = name + 'Factory'
                # Use the Factory class name to create an instance of it from the current module file 
                factory_instance = getattr(current_module, factory_name)()
                self.factories.append((name, factory_instance))
            self.initialized = True
    
    # A Factory method that organizes everything together
    def make_drink(self):
        print('Available drinks: ')
        for f in self.factories:
            print(f[0])
        
        s = input(f'Please pick drink (0-{len(self.factories) - 1}): ')
        idx = int(s)
        s = input(f'Specify amount: ')
        amount = int(s)
        print(amount)
        return self.factories[idx][1].prepare(amount)


if __name__ == '__main__':
    hdm = HotDrinkMachine()
    hdm.make_drink()




# EXERCISE
# You are given a class called Person . The person has two attributes: id , and name .
# Implement a PersonFactory that has a non-static  create_person() method that takes a person's name and 
# returns a person initialized with this name and an id.
# The id of the person should be set as a 0-based index of the object created. 
# So, the first person the factory makes should have id=0, second id=1 and so on.

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class PersonFactory:
    id = 0 # class attribute
    def create_person(self, name):
        p = Person(PersonFactory.id, name)
        # The class attribute 'id' is used in creating a new instance because different Factory instances
        # will share the same class attribute and its state is preserved in the class!
        PersonFactory.id += 1
        return p