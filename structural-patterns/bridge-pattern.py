# The Bridge Design Pattern is all about connecting Components through abstraction.
# The Bridge prevents a 'cartesian product' complexity explosion. For example, suppose you have a Base
# Class called 'ThreadScheduler' that can be preemptive or cooperative and can run on Windows or Linux. 
# (These are Operating System multitasking concepts - in Preemptive multitasking, the operating system 
# can initiate a context switching from the running process to another process. In other words, the 
# operating system allows stopping the execution of the currently running process and allocating the CPU 
# to some other process. The OS uses some criteria to decide for how long a process should execute before 
# allowing another process to use the operating system. In Cooperative multitasking, the operating system 
# never initiates context switching from the running process to another process. A context switch occurs 
# only when the processes voluntarily yield control periodically or when idle or logically blocked to allow 
# multiple applications to execute simultaneously.) 
# Here, you end up with a 2x2 scenario of: WindowsPreemptive, WindowsCooperative, LinuxPreemptive and 
# LinuxCooperative scheduling. The Bridge pattern attemps to avoid this combinatorial explosion typically
# by introducing an Interface for Platform (Windows or Linux) Scheduling that can be used by 'ThreadScheduler'

# A Bridge is a mechanism that decouples an interface or abstraction (hierarchy) from an 
# implementation (hierarchy). Both can exist as hierarchies. The Bridge pattern is essentially a stronger
# form of encapsulation! 

# Suppose you have a drawing application that can draw shapes like circles and squares. It can render
# these shapes in different forms such as pixel or raster, vector. Instead of creating four seperate classes
# for this purpose like VectorCircle, VectorSquare, RasterCircle, RasterSquare etc, we can reduce the complexity
# by following the Bridge pattern.

from abc import ABC # for creating abstract base classes with abstract methods, we import and inherit this class

class Renderer(ABC):
    # abstract method - A method without a body
    def render_circle(self, radius):
        pass
    # abstract method - A method without a body
    def render_square(self, side):
        pass

# Keep in mind that the 'Renderer' Hierarchies defined below are tied to the shapes that they can create.
# Addition of any new shape as a feature for the drawing app will require the implementation of the shape in
# every type of the 'Renderer' class Hierarchy - VIOLATION OF THE OPEN-CLOSED PRINCIPLE. But unfortunately,
# nothing can be done to improve this because of the objective being reduction of "complexity explostion"!
class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(f'Drawing a circle of radius {radius}')
    def render_square(self, side):
        print(f'Drawing a square of side {side}')


class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(f'Drawing pixels for a circle of radius {radius}')
    def render_square(self, side):
        print(f'Drawing pixels for a square of side {side}')


class Shape:
    # Core of the Bridge design pattern - connect the renderer to the shape
    def __init__(self, renderer):
        self.renderer = renderer
    def draw(self): pass
    def resize(self, factor): pass


class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer) # call the Base class (Shape) initializer with the passed in 
        # 'renderer' object which can be instance of any one of 'VectorRenderer' or 'RasterRenderer'
        self.radius = radius
    def draw(self):
        # Use the Bridge pattern to make the connection between a renderer and a shape class Hierarchy, then 
        # use this connection to utilize the functionalities of renderer from within the shape class
        self.renderer.render_circle(self.radius)
    def resize(self, factor):
        self.radius *= factor

    
if __name__ == '__main__':
    # The Bridge pattern just connects two Hierarchies of different classes through parameters
    # usually through the initializer.
    raster = RasterRenderer()
    vector = VectorRenderer()
    # circle = Circle(raster, 5)
    circle = Circle(vector, 5)
    circle.draw()
    circle.resize(2)
    circle.draw()




# EXERCISE

# TODO: reimplement Shape, Square, Triangle and Renderer/VectorRenderer/RasterRenderer such that
# 'str(Triangle(RasterRenderer()))'  returns "Drawing Triangle as pixels" 

class Renderer(ABC):
    @property
    def what_to_render_as(self):
        return None

class VectorRenderer(Renderer):
    @property
    def what_to_render_as(self):
        return 'lines'
        
class RasterRenderer(Renderer):
    @property
    def what_to_render_as(self):
        return 'pixels'

class Shape:
    def __init__(self, name, renderer):
        self.renderer = renderer
        self.name = name
    def __str__(self):
        return 'Drawing {} as {}'.format(self.name, self.renderer.what_to_render_as)
        
class Square(Shape):
    def __init__(self, renderer):
        super().__init__('Square', renderer)

class Triangle(Shape):
    def __init__(self, renderer):
        super().__init__('Triangle', renderer)