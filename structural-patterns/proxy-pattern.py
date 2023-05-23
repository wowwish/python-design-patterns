# The Proxy Design Pattern has many different Incarnations!
# Assume that you are calling a function 'foo.Bar()'. This call assumes that the method 'Bar()' and the
# object 'foo' are present within the same process of the python interpretor running some python code. 
# But, what if, later on, you want to put all your 'Foo' class related operations into a seperate
# process ? can you avoid changing the code while a python interpreter process in already running with
# your code ? This is where the Proxy Design Pattern comes to the rescue!

# A Proxy is a class that functions as an Interface to a particular resource (another class). A Proxy has the
# same interface as its underlying object. To create a Proxy, simply replicate the existing interface of an 
# object and add relevant functionality to the redefined member functions of the Proxy. The resource may 
# be remote, expensive to construct, or may require logging or some other functionality. The way that the
# Proxy class implements this is typically by keeping the resource unchanged

# A Proxy is used to provide a pre-existing Interface (class) with radically different behaviour.
# Such a Proxy is called as a "Communication Proxy". Other incarnations of the Proxy Pattern include:
# "Logging Proxy", "Virtual Proxy", "Guarding Proxy", "Cache Proxy" ... each with different behaviours!


# PROTECTION PROXY (Guarding Proxy) - A Proxy that controls access to a particular resource (like user login
# check for access to features)
class Car:
    def __init__(self, driver):
        self.driver = driver
    # suppose you want to have age control and prevent people too young from driving. 
    # Assuming that this version of the code is already running somewhere or cannot be modified, we
    # have to create a Proxy of this class that implements this new behaviour (without violating the 
    # open-closed principle)
    def drive(self):
        print(f'Car is being driven by {self.driver.name}')

class Driver:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# The Proxy class
class CarProxy:
    def __init__(self, driver):
        self.driver = driver
        # instantiate the source Class for the Proxy as a private internal attribute
        self._car = Car(driver)
    def drive(self): # modified from the source class, now with age-control
        if self.driver.age >= 16:
            self._car.drive()
        else:
            print('Driver too young')

# if __name__ == '__main__':
    # driver = Driver('John', 20)
    # driver = Driver('John', 12)
    # car = Car(driver)
    # car = CarProxy(driver)
    # car.drive()




# VIRTUAL PROXY - A Proxy for a Class that is not fully initialized. It behaves like the class it represents
# but works differently behind the scenes and can provide modified functionality of the 
# underlying object.

# For example, consider an application that manages bitmap images or photos

class BitMap:
    def __init__(self, filename):
        self.filename = filename
        # The image is loaded everytime this class is instantiated irrespective of whether it is later used
        # for drawing. This can be a wasteful and expensive use of memory which can be prevented by implementing
        # a Proxy over this class when this class has restrictions on modification (such as when a python 
        # interpretter process is already running with this code!) following the Open-Closed Principle.
        print(f'Loading image from {self.filename}')

    def draw(self):
        print(f'Drawing image {self.filename}')


# We can implementing the "Lazy Loading" of the image file using a Virtual Proxy
class LazyBitMap:
    def __init__(self, filename):
        self.filename = filename
        self._bitmap = None # A private internal attribute

    def draw(self):
        # Lazy Laoading - Load the image file only when the draw() method is actually called!
        if not self._bitmap:
            self._bitmap = BitMap(self.filename)
        self._bitmap.draw()

# A function to draw a given 'BitMap' instance
def draw_image(image):
    print('About to draw image')
    image.draw()
    print('Done drawing image')


if __name__ == '__main__':
    # bmp = BitMap('facepalm.jpg')
    bmp = LazyBitMap('facepalm.jpg')
    # Notice that loading of image only happens once with the Virtual Proxy 'LazyBitMap' instance
    draw_image(bmp)
    draw_image(bmp)





# PROXY VS DECORATOR

#   * A Proxy provides an identical Interface to the underlying class whereas a Decorator provides an
#     enhanced interface to the underlying class with additional functionality.
#   * A Decorator typically aggregates (or has a reference to the underlying object) what it is decorating. 
#     A Proxy doesn't have to have a reference to its underlying object. A Proxy can work with even non-materialized
#     (un-inistantiated or non-existent or lazy) objects




# EXERCISE

# You are given the 'Person' class and asked to write a 'ResponsiblePerson' proxy that does the following:
#   * Allows person to drink unless they are younger than 18 (in that case, return "too young")
#   * Allows person to drive unless they are younger than 16 (otherwise, "too young")
#   * In case of driving while drink, returns "dead", regardless of age

class Person:
    def __init__(self, age):
        self.age = age

    def drink(self):
        return 'drinking'

    def drive(self):
        return 'driving'

    def drink_and_drive(self):
        return 'driving while drunk'

class ResponsiblePerson:
    def __init__(self, person):
        self._person = person
    # Setup the age of the 'Person' instance as a property with its own setter in the Proxy class
    @property
    def age(self):
        return self._person.age
    
    @age.setter
    def age(self, value):
        self._person.age = value

    def drink(self):
        if self.age < 18:
            return 'too young'
        else:
            self._person.drink()
    
    def drive(self):
        if self.age < 16:
            return 'too young'
        else:
            self._person.drive()
   
    def drink_and_drive(self):
        return 'dead'
    