# Interface Segegation Principle states 


# import Base Class and decorator to be used for implementing abstract methods (methods without a body 
# that must be implemented in the child classes). 
from abc import ABC, abstractmethod

class Machine:
    def print(self, document):
        raise NotImplementedError
    def fax(self, document):
        raise NotImplementedError
    def scan(self, document):
        raise NotImplementedError
    

class MultiFunctionPrinter(Machine):
    def print(self, document):
        print('printing...')

    def fax(self, document):
        print('sending...')

    def scan(self, document):
        print('scanning...')

# An old-fashioned printer will not have all the functionalities of a modern printer. Hence
class OldFashionedPrinter(Machine):
    def print(self, document):
        print('printing...')
    # The functionalities (methods) below are not features of an old fashioned printer
    # Hence, they are left in their un-implemented form, but are still accessible and can be called 
    # because OldFashionedPrinter inherits from Machine!
    # THIS BREAKS THE INTERFACE SEGREGATION PRINCIPLE!
    def print(self, document):
        pass

    def print(self, document):
        """Not Supported"""
        raise NotImplementedError
    
# A solution to this issue is to split the 'Machine' interface into seperate (more granular) interfaces

class Printer(ABC):
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def print(self, document):
        pass

class Scanner(ABC):
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def scan(self, document):
        pass

class Fax(ABC):
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def fax(self, document):
        pass

def PhotoCopier(Printer, Scanner): # Multiple Inheritance
    def print(self, document):
        pass
    def scan(self, document):
        pass

# You can also create an Interface that can combines the functionalities of multiple other
# interfaces and can be used as a Base Class!
def MultiFunctionDevice(ABC):
    # Override the inherited methods and declare them as abstract methods
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def scan(self, document):
        pass
    @abstractmethod # A decorator to declare abstract method (method without a body that must be
    # implemented compulsarily in the inheriting child classes)
    def fax(self, document):
        pass

# Now, we can inherit the newly created combination Base Class!
def MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer =  printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)