# The use of this pattern almost always signifies a design smell. The original GoF authors pointed to
# this pattern when asked about a design pattern which they were in favor of dropping out of their book!

# REMEMBER, THE SINGLETON PATTERN IS AN ANTI-PATTERN, A DESIGN SMELL AND NOT SOMETHING YOU WOULD WANT
# TO USE IN YOUR SOFTWARE DESIGN!

# However, for some components in the system, it makes sense to only initialize one instance in the
# system. Examples include:
#   * Database Repository - Loading some data from a database at the begining of the program and then
#   keeping it accessible while the program runs
#   * Object Factories - Do you need a Factory for every Object when you can simply have one Factory
#   with multiple static methods for every type of Object ? Keep in mind that an Object Factory is
#   stateless (does not contain any attributes worth assigning) and can simply function through static
#   methods.

# Singletons are a bad Design Pattern because:
#   * Their initializer (Constructor) call can be expensive
#   * We expect only one instance to be created from the Singleton and provide everyone with the same
#   kind of instance of the Singleton.
#   * We typically have to prevent users from creating any additional copies of the Singleton instance.
#   * We need to take care of Lazy instantiation (nobody gets to instantiate the Singleton unless its
#   functionality is really needed or some part of the code asks for it)

# Sometimes, singleton classes are unavoidable: examples of Singleton classes in python include 
# 'None', 'True' and 'False'

# A Singleton is any Component (class) which is instantiated only once.


# INSTANTIATING A SINGLETON CLASS (ONLY ONE OBJECT CAN BE CREATED THROUGHT RUNTIME)

# USING A SINGLETON ALLOCATOR METHOD (CALLS THE INSTANTIATIOR MULTIPLE TIMES - NOT IDEAL APPROACH):

import random


# A Singleton (class with only one instance)
class Database:
    _instance = None  # Flag to check if class has been instantiated

    # Whenever a class is instantiated __new__ and __init__ methods are called.
    # __new__ method will be called when an object is created and __init__ method
    # will be called to initialize the object. In the base class object, the __new__
    # method is defined as a static method which requires to pass a parameter 'cls'.
    # 'cls' represents the class that is needed to be instantiated, and the compiler
    # automatically provides this parameter at the time of instantiation.

    # If both __init__ method and __new__ method exists in the class,
    # then the __new__ method is executed first and decides whether to
    # use __init__ method or not, because other class constructors can
    # be called by __new__ method or it can simply return other objects
    # as an instance of this class.
    # Here, we are overriding the in-built __new__() method of the 'object' class
    # of python, which is used to create a new empty (raw) unconfigured instance of
    # a class.

    # The singleton allocator method - only creates a new instance if the class is not
    # already instantiated
    def __new__(cls, *args, **kwargs):
        # The __new__() is a static method of the object class.
        # The first argument of the __new__() method is the class of the new
        # object that you want to create.

        # The __new__() method  also requires '*args' and '**kwargs' arguments
        # that must match the parameters of the __init__() of the class.

        # The __new__() method should return a new object of the class. But it doesn't have to.

        # When you define a new class, that class implicitly inherits from the in-built 'object'
        # class of python (the root class for all classes in python). It means that you can override
        # the __new__ static method and do something before and after creating a new instance of the class.

        # To create the object of a class, you call the super().__new__() method.
        # Technically, you can call the object.__new__() method to create an object manually.
        # However, you need to call the __init__() yourself manually after. Python will not call the
        # __init__() method automatically if you explicitly create a new object using the
        # object.__new__() method.
        if not cls._instance:  # class has not been initialized/insatantiated yet
            # initialize the instance of the class with the __new__() method of the Parent class
            # (the built-in 'object' class).
            # the 'object.__new__()' method will throw an error that object() takes no parameters in
            # Python > version 2.6 when '*args' and '**kwargs' are passed in as arguments. However,
            # Your Singleton class which inherits the 'object' class will have to provide '*args' and
            # '**kwargs' as arguments in its __new__() method!
            cls._instance = super().__new__(cls)
        # The __new__() method should return allocated singleton object
        return cls._instance

    # The in-built initializer __init__() is called immediately after __new()__ is called.
    # Notice that this method is called twice since two objects of 'Database' class are created
    # But, using out implementation of the __new__() (singleton allocator method), we are able
    # to prevent more than one object being created for the Singleton 'Database' class.
    def __init__(self):
        id = random.randint(1, 101)
        print('id = ', id)
        # print('Loading a database from file')


# KEEP IN MIND THAT THE __init__() METHOD IS STILL CALLED TWICE EVEN THOUGH THE SINGLETON CLASS CREATION
# HAPPENS ONLY ONCE WHEN IT IS INSTANTIATED TWICE!
# if __name__ == '__main__':
    # The instantiation of the Singleton will produce two random numbers that are different because, the
    # even though the __new__() method is not called only in the first instantiation, the __init__() method
    # will be called on both the instantiations and will create random numbers both the times.
    # d1 = Database()
    # d2 = Database()
    # The 'is' operator is used instead of '==' to check for the same object in memory
    # print(d1 is d2)


# SINGLETON DECORATOR (A GOOD APPROACH)

# The decorator is a function that takes in another function as argument and returns a function
# that has additional functionality along with the input function. A decorator can be a function
# or a class. This decorator below takes a Class as an argument and adds additional functionality
# to it (the 'get_instance()' method in this case).
def singleton(class_):
    # Keep the single instance for every Class that is decorated with this decorator
    # in this dictionary as value, with the Class name as key
    instances = {}
    # inner wrapper function of the decorator
    def get_instance(*args, **kwargs):
        # use '*args* and '**kwargs* to allow the inner wrapper
        # function of the decorator to be flexible with (or without) positional and keyword arguments
        # if a requested instance for a Class is not already in the instance dictionary,
        # we create a new instance of the requested Class, add it to the instance dictionary.
        # and return it. Otherwise, the existing instance from the instance dictionary is returned.
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    # The decorator returns its inner wrapper function get_instance()
    return get_instance


# Using the 'singleton' Decorator that we just built
@singleton # Now Datbase = singleton(Database)
class Database:
    def __init__(self):
        # This will be prnted only once because, the decorator takes care of preventing the
        # initialization of multiple objects of the class that is passed to it
        print('Loading Database')


# YOU CAN SEE THAT HERE, THE INITIALIZER (CONSTRUCTOR) OF THE DECORATED CLASS DOES NOT
# GET CALLED SEVERAL TIMES
# if __name__ == '__main__':
#     d1 = Database()
#     d2 = Database()
#     print(d1 is d2)





# SINGLETON META-CLASSES (A GOOD APPROACH)

# In python version 3, an Object's Class (obj.__class__) and Type ('type(obj)') are the same.
# In python version 3, everything is an Object including Classes themselves.
# The Type ('type(obj)') of in-built classes in Python (like int, float, dict, list, tuple) is 'type'
# The Type of 'type' is also 'type' itself!
# 'type' is a metaclass of which all Classes in python 3 are an instance, just like objects are instances
# of a class.
# When you create an instance 'x' of some class 'Foo', 'x' becomes an instance of 'Foo'. However, 'Foo'
# is an instance of 'type' and 'type' is an instance of 'type' metaclass itself!

# The built-in type() function in python 3 can be used to not just check the Class that an instance (Object) 
# belongs to, but can also be used to create an instance of the 'type' Metaclass (dynamic creation of new
# classes during runtime) like so: 
#   type(<name>, <bases>, <dct>) 
# Here:
#   *   <name> is a string that specifies the class name
#   *   <bases> is a tuple of the base classes from which the newly created class will inherit 
#       (added as the .__bases__ attribute of the newly created class)
#   *   <dct> is a namespace dictionary of the class body definitions (attributes and methods) which
#       will be stored as .__dict__ property of the newly created class  



# Examples of Creating Metaclasses:

def f(obj):
    print('attr=', obj.attr)
Foo = type('Foo', (), {})
Bar = type('Bar', (Foo,), {'attr': 100, 'attr_val': f})
x = Bar()
print(x.attr) # 100
x.attr_val()
print(x.__class__)
print(x.__class__.__bases__)

# Running the above lines in python 3 is equivalent to running:
def f(obj):
    print('attr=', obj.attr)
class Foo:
    pass
class Bar(Foo):
    attr = 100
    attr_val = f
x = Bar()
x.attr_val()


# When a Class 'Foo' is instantiated in python 3, the __call__() method of the class's parent (which could be
# the 'type' metaclass for a normal class) will be invoked. This __call__() method in turn invokes
# the __new__() and __init__() methods of the Parent class of 'Foo' (which could be 'type' metaclass for 
# classes which donot have any other ancestry). But if the class 'Foo' does define these two methods,
# Foo's __new__() and __init__() methods will be invoked. This allows for customized behaviour when 
# instantiating 'Foo' like so:

def new(cls):
     x = object.__new__(cls)
     x.attr = 100
     return x

Foo.__new__ = new  

# This modifies the instantiation behavior of class Foo: each time an instance of 'Foo' is created, by 
# default it is initialized with an attribute called 'attr', which has a value of 100. (Code like this would 
# more usually appear in the __init__() method and not typically in __new__(). 

# However, you can’t reassign the __new__() method of the 'type' metaclass. Python doesn’t allow it.
#  Essentially, instead of mucking around with the type metaclass, you can define your own metaclass, 
# which derives from type, and then you can muck around with that instead.

# Creating a custome Metaclass:
class Meta(type):
    def __new__(cls, name, bases, dict):
        # The super() call takes two optional arguments: a sub-class name and an object that
        # is an instance of that sub-class.
        x = super().__new__(cls, name, bases, dict)
        x.attr = 100
        return x
    
# Another way to create a custom metaclass:
# class Meta(type):
#     def __init__(cls, name, bases, dict):
#         cls.attr = 100
    
# The definition header 'class Meta(type):' specifies that Meta derives from type. Since type is a metaclass, 
# that makes Meta a metaclass as well.
# Note that a custom __new__() method has been defined for 'Meta'. It wasn’t possible to do that to the 'type' 
# metaclass directly. The __new__() method does the following:
#   * Delegates via super() to the __new__() method of the parent metaclass (type) to actually create a 
#     new class
#   * Assigns the custom attribute 'attr' to the class, with a value of 100
#   * Returns the newly created class

# Now we can define a new class 'Foo' and specify that its metaclass is the custom metaclass 'Meta', 
# rather than the standard metaclass 'type'. This is done using the 'metaclass' keyword in the class 
# definition as follows:
class Foo(metaclass = Meta):
    pass

# Metaclass that inherits from the 'type' Class
class Singleton(type):
    _instances = {}
    # Overriding the default behavior of the __call__() method of the metaclass
    def __call__(cls, *args, **kwargs):
        # Here, 'cls' corresponds to the class that inherits this metaclass
        if cls not in cls._instances:
            # The super() call takes two optional arguments: a sub-class name and an object that
            # is an instance of that sub-class. Here, we are calling the __call__() method of the 
            # 'type' metaclass which this 'Singleton' class inherits
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Database(metaclass=Singleton):
    def __init__(self):
        print('Loading database')

# if __name__ == '__main__':
#     d1 = Database()
#     d2 = Database()
#     print(d1 is d2)




# MONOSTATE IMPLEMENTATION OF SINGLETON (NOT A RECOMMENDED APPROACH)

# In this variation of the Singleton pattern, we put all the state of an Object into a static variable
# and allow people to create new objects, thereby making the new instances (Objects) one and the same
# (the subseqent new instances will be referring to the first instance of the class)

class CEO:
    # A single static shared state of the Class which is shared by all instances of this class.
    # Any modification of these attributes by one object will be reflected in all objects of this class.
    _shared_state = {
        'name': 'Steve',
        'age': 55
    }

    def __init__(self):
        # Whenever you initialize or construct an instance of this class, you will always be referring
        # to the same set of attributes
        self.__dict__ = self._shared_state

    def __str__(self):
        return f'{self.name} is {self.age} years old'

# Package the Monostate as a Base class that can be inherited
class Monostate:
    _shared_state = {}
    # oerriding the __new__() method that will be invoked before __init__() during instantiation
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

class CFO(Monostate):
    def __init__(self):
        self.name = ''
        self.money_managed = 0

    def __str__(self):
        return f'{self.name} manages ${self.money_managed}'

if __name__ == '__main__':
    ceo1 = CEO()
    print(ceo1)
    ceo2 = CEO()
    # After setting the shared attribute, all objects of the class reflect the same value
    ceo2.age = 77
    print(ceo1)
    print(ceo2)
    cfo1 = CFO()
    cfo1.name = 'Sheryl'
    cfo1.money_managed = 1
    print(cfo1)
    cfo2 = CFO()
    # The changes below will become reflected in both 'cfo1' and 'cfo2' because of shared state
    # Remember that new set of attributes are not created, the same attributes are referenced in the
    # new instances. Hence, any change in the referenced attribute will be a change in the original
    cfo2.name = 'Ruth'
    cfo2.money_managed = 10
    print(cfo1, cfo2, sep="\n")



# REMEMBER, THE SINGLETON PATTERN IS AN ANTI-PATTERN, A DESIGN SMELL AND NOT SOMETHING YOU WOULD WANT
# TO USE IN YOUR SOFTWARE DESIGN!


# SINGLETON TESTABILITY

import unittest

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        self.population = {}
        f = open('capitals.txt', 'r')
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            self.population[lines[i].strip()] = int(lines[i+1].strip())
        f.close()

class SingletonRecordFinder:
    def total_population(self, cities):
        result = 0
        for c in cities:
            # An instance of the Singleton class 'Database' is created (first iteration) or 
            # referenced (second iteration onwards) for every city passed to this method and then, 
            # the population is added to the result
            result += Database().population[c]
        return result

class ConfigurableRecordFinder:
    def __init__(self, db=Database()):
        self.db = db
    def total_population(self, cities):
        result = 0
        for c in cities:
            # Here, the database is created only once and it is used everytime the loop runs 
            result += self.db.population[c]
        return result

# A dummy database with predictable values for testing
class DummyDatabase:
    population = {
        'alpha': 1,
        'beta': 2,
        'gamma': 3
    }
    def get_population(self, name):
        return self.population[name]

# Unit Testing a Singleton
class SingletonTest(unittest.TestCase):
    def test_is_singleton(self):
        db1 = Database()
        db2 = Database()
        self.assertEqual(db1, db2)

    def test_singleton_total_population(self):
        rf = SingletonRecordFinder()
        names = ['Seoul', 'Mexico City']
        # Since an instance of Database() is created to check for the population of individual
        # cities, this approach of testing becomes dangerous for a live database that keeps
        # updating itself in production! We can instead use dummy values from a dummy Database
        # and use it to test
        tp = rf.total_population(names)
        self.assertEqual(17500000 + 17400000, tp)

    # Instantiate the Singleton Dummy Database for testing
    ddb = DummyDatabase()

    def test_dependent_total_population(self):
        crf = ConfigurableRecordFinder(self.ddb)
        self.assertEqual(3, crf.total_population(['alpha', 'beta']))


if __name__ == '__main__':
    unittest.main()



# EXERCISE

def is_singleton(factory):
    obj1 = factory()
    obj2 = factory()
    if (obj1 is obj2):
        return 'true'
    else:
        return 'false'