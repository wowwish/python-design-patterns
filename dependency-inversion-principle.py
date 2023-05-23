# Dependency Inversion Principle

# THIS PRINCIPLE DOES NOT RELATE TO DEPENDENCY INJECTION !

# The Dependency Inversion Principle states that higher Level Instances or modules should not directly 
# depend on Lower level modules or interfaces, they should instead depend on abstractions.
# High-level modules, which provide complex logic, should be easily 
# reusable and unaffected by changes in low-level modules, which provide utility features. Use 
# abstraction that decouples the high-level and low-level modules from each other.
# Dependency Inversion Principle suggests to use abstract interfaces rather than implemented classes
# so that you can swap the Interfaces easily.

# An enumeration is a set of symbolic names (members) bound to unique values
from enum import Enum
# import Base Class and decorator to be used for implementing abstract methods (methods without a body 
# that must be implemented in the child classes). 
from abc import ABC, abstractmethod

# The enum members have names and values (the name of Color.RED is RED, the value of Color.BLUE is 3, etc.)
class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2

class Person:
    def __init__(self, name):
        self.name = name

# A low-level interface with utility-functions declared as abstract methods that helps to uphold
# the dependency inversion principles. If the internal storage in the 'Relationships' class changes,
# we can simply modify these utility methods for continuation!
class RelationshipBrowser(ABC):
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def find_all_children_of(self, name): # Utility method to add in the low-level interfaces/classes
        # to keep the Dependency Inversion Principle
        pass

# LOW-LEVEL CLASS/INTERFACE/MODULE
# We Inherit the utility interface to keep up the Dependency Inversion Principle!
class Relationships(RelationshipBrowser):
    def __init__(self):
        self.relations = []
    
    def add_parent_and_child(self, parent, child):
        self.relations.append(
            (parent, Relationship.PARENT, child)
        )
        self.relations.append(
            (child, Relationship.CHILD, parent)
        )
    # abstract method implementation in the inheriting sub-class
    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name # makes this function return a generator

# class Research:
    # Accessing the internal storage mechanism and data structure of 'Relatonships' class
    # If the internal list that store the relationships (the list 'self.relations' of class
    # type 'Relationships') is modified, for example, to a dictionary instead of a list, it will
    # break all the sub-classes that depend on it as well as other clasess that use its instances.
    # THIS BREAKS THE DEPENDENCY INVERSION PRINCIPLE!

    # relations = relationships.relations
    
    # The core functionality is implemented in this low level class
    # This makes the higher level classes to depend on this low level class and breaks the
    # Dependency Inversion Principle!
    # def __init__(self, relationships):
        # for r in relations:
        #     if r[0].name == 'John' and r[1] == Relationship.PARENT:
        #         print(f'John has a child called {r[2].name}.')

# HIGH-LEVEL CLASS/INTERFACE/MODULE
class Research:
    def __init__(self, browser):
        for p in browser.find_all_children_of('John'):
            print(f'John has a child called {p}')


parent = Person('John')
child1 = Person('Chris')
child2 = Person('Matt')

# Instantiating the low-level Class and adding relationships
relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

# High level module 
Research(relationships)