# Complicated objects in the real world (like cars) are never designed from scratch.
# They reiterate existing designs.
# This design pattern similarly, uses an existing (partially or fully constructed)
# design (also called a Prototype) and customizes it for use.
# We make a 'deep copy' (clone) of the Prototype and customize it.
# We also make the cloning convenient (eg: by using a Prototype Factory - Ask a Factory to customize
# a pre-defined Prototype design)

# To implement this design pattern, create a Prototype (partially constructed Object) and store 
# it somewhere. Deep copy this Prototype and then customize the resulting instance (Object).
# A Factory (any class, method or component that creates a new object) provides a convenient
# API for customizing and using Prototypes (create customized clones)!

import copy  # for deep-copying objects


class Address:
    def __init__(self, street_address, city, country):
        self.street_address = street_address
        self.city = city
        self.country = country

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.country}'


class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self):
        return f'{self.name} lives at {self.address}'


address = Address('123 London Road', 'London', 'UK')
# A Prototype
john = Person('John', address)
print(john)
# Unfortunately here, 'john' and 'jane' refer to the same object (this is not a deep copy)
# jane = john
# jane.name = 'Jane'
# We can try to fix this by doing something like this:
# But this too has repercussions like below (any change in the 'address' of 'jane' is reflected in 'john'):
# jane = Person('Jane', address)
# jane.address.street_address = '123B London Road'

# Perform a shallow-copy causes any reference to another object to be copied over as a reference
# Thus, the following shallow-copy will lead to carry-over effect on the 'address' object since it
# is referenced in the 'john' object and the same reference is copied over to the 'jane' object
# jane = copy.copy(john)
# Performing a Deep-copy of a Prototype object
jane = copy.deepcopy(john)
jane.name = 'Jane'
jane.address.street_address = '124 London Road'
print("---")
# Due to lack of deep-copy, the change in 'jane' is actually a change in 'john' as well
print(john)
print(jane)


# PROTOTYPE FACTORY

# It is quite often inconvenient to make deep-copies of instances (Objects) manually using 'copy.deepcopy()'
# It would be nice to have a Factory to package pre-defined Prototypes rather than performing deep-copies
# and customizations on the Prototype manually.


class OfficialAddress:
    def __init__(self, street_address, city, suite):
        self.street_address = street_address
        self.city = city
        self.suite = suite
    
    def __str__(self):
        return f'{self.street_address}, Suite #{self.suite}, {self.city}'

class Employee:
    def __init__(self, name, address):
        self.address = address
        self.name = name

    def __str__(self):
        return f'{self.name} works at {self.address}'


# Prototype Factory class
class EmployeeFactory:
    # Two Prototypes (static objects)
    main_office_employee = Employee(
        '', OfficialAddress('123 East Drive', 0, 'London'))
    aux_office_employee = Employee(
        '', OfficialAddress('123B East Drive', 0, 'London'))

    # Factory Methods for creating copies (cloning) of 'Employee' objects
    # We are creating Factory methods for a main office employee and an auxillary
    # office employee here.
    @staticmethod
    # This is a utility method to perform deep-copy!
    # This dunder method (double underscores at the start of method name) is not
    # supposed to be consumed (invoked) from outside the EmployeeFactory class.
    def __new_employee(proto, name, suite):
        result = copy.deepcopy(proto)
        result.name = name
        result.address.suite = suite
        return result

    # These two are Factory methods that make use of the utility method above to create
    # customized copies of the 'Employee' Prototype.
    # Prototype Factory method 1
    @staticmethod
    def new_main_office_employee(name, suite):
        return EmployeeFactory.__new_employee(
            EmployeeFactory.main_office_employee,
            name, suite
        )
    # Prototype Factory methods 2
    @staticmethod
    def new_aux_office_employee(name, suite):
        return EmployeeFactory.__new_employee(
            EmployeeFactory.aux_office_employee,
            name, suite
        )

# Create objects using the Prototype Factory methods
john = EmployeeFactory.new_main_office_employee('John', 101)
jane = EmployeeFactory.new_aux_office_employee('Jane', 500)

print(john)
print(jane)



# EXERCISE 

# implement Line.deep_copy()  to perform a deep copy of the given Line  object. 
# This method should return a copy of a Line that contains copies of its start/end points.

import copy

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start=Point(), end=Point()):
        self.start = start
        self.end = end

    def deep_copy(self):
        new_starting_point = Point(self.start.x, self.start.y)
        new_ending_point = Point(self.end.x, self.end.y)
        return Line(new_starting_point, new_ending_point)