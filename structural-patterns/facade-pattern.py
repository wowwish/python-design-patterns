# Pronounced as 'Fuh-saad'
# The Facade Design Pattern is used to expose several components (classes) using a single Interface
# This Design Pattern is used to balance complexity with presentation and usability
# For example, a typical home has many sub-systems (electrical, sanitation etc) and a complex structure
# (the floor could have several layers), but the end user or customer is not exposed to these internals
# Similarly with Software, many systems work to provide flexibility, but, API consumers want it to "just work"

# A Facade provides a simple, easy to understand, user interface over a large and sophisticated body of code.
# It provides a simplified API over a set of classes.
# You can also optionally expose the internals of the sub-systems through the Facade if required (allow access 
# to complex internal APIs similar to escalation of policies, when the user needs to use them).

# As an example, consider the command console (terminal/command prompt) - it consists of a buffer (where all the characters to be 
# displayed to the console screen are stored), view ports (that show only the last few lines or a chunk of the 
# information from the buffer)


class Buffer:
    def __init__(self, width=30, height=20):
        self.width = width
        self.height = height
        # initialize the buffer with spaces
        self.buffer = [' '] * (width * height)
    # support for indexing - get a character at a particular position in the buffer
    def __getitem__(self, item):
        # Since our self.buffer is a list of characters, we use the __getitem__() of the list instance (object)  
        return self.buffer.__getitem__(item)

    def write(self, text):
        self.buffer += text


# Used to show a chunk of the Buffer on screen
class ViewPort:
    def __init__(self, buffer=Buffer()):
        self.buffer = buffer
        self.offset = 0
    # get a character at a particular index within this viewport (the 'offset' attribute takes care of getting
    # the character at the index of the chunk of the buffer that this viewport holds)
    def get_char_at(self, index):
        return self.buffer[index+self.offset]
    # add content to the underlying buffer through the viewport
    def append(self, text):
        self.buffer.write(text)


# A Facade (neat, clean and usable interface) for the 'ViewPort' and 'Buffer' classes (sub-systems)
# Here we hide all the complexity associated with functionalities and expose simple methods (High-level APIs) 
# to the user
class Console:
    def __init__(self):
        b = Buffer()
        # create a lists to hold 'Buffer' and 'ViewPort' instances so we can append additional instances to them
        self.current_viewport = ViewPort(b)
        self.buffers = [b]
        self.viewports = [self.current_viewport]
    
    # method to write to the console (currently selected ViewPort instance)
    # This is a high-level API that connects to the functionality of a lower-level API in the 'Buffer' instance
    def write(self, text):
        self.current_viewport.buffer.write(text)

    # method to get the character at a particular index within the current 'ViewPort' instance.
    # This is a high-level API that connects to the functionality of a lower-level API in the 'Buffer' instance
    def get_character_at(self, index):
        self.current_viewport.buffer.__getitem__(index)


if __name__ == '__main__':
    c = Console()
    c.write('hello')
    ch = c.get_character_at(0)




# EXERCISE

# A magic square is a square matrix of numbers where the sum in each row, each column, and each of the two 
# diagonals is the same.
# You are given a system of 3 classes that can be used to make a magic square. The classes are:

#   * Generator: this class generates a 1-dimensional list of random digits in range 1 to 9.
#   * Splitter: this class takes a 2D list and splits it into all possible arrangements of 1D lists. 
#     It gives you the columns, the rows and the two diagonals.
#   * Verifier: this class takes a 2D list and verifies that the sum of elements in every sublist is the same.

# Please implement a Façade class called 'MagicSquareGenerator'  which simply generates the magic square of a 
# given size.

from random import randint

class Generator:
  def generate(self, count):
    return [randint(1,9) for x in range(count)]

class Splitter:
  def split(self, array):
    result = []

    row_count = len(array)
    col_count = len(array[0])

    for r in range(row_count):
      the_row = []
      for c in range(col_count):
        the_row.append(array[r][c])
      result.append(the_row)

    for c in range(col_count):
      the_col = []
      for r in range(row_count):
        the_col.append(array[r][c])
      result.append(the_col)

    diag1 = []
    diag2 = []

    for c in range(col_count):
      for r in range(row_count):
        if c == r:
          diag1.append(array[r][c])
        r2 = row_count - r - 1
        if c == r2:
          diag2.append(array[r][c])

    result.append(diag1)
    result.append(diag2)

    return result

class Verifier:
  def verify(self, arrays):
    first = sum(arrays[0])

    for i in range(1, len(arrays)):
      if sum(arrays[i]) != first:
        return False

    return True

class MagicSquareGenerator:
  def generate(self, size):
    gen = Generator()
    check = Verifier()
    extract = Splitter()
    # Run a loop till a magic matrix is built
    # use the 'Generator' instance to build rows of random numbers and add the rows to an empty list
    # then extract the different sums to be checked for the generated magic matrix using instance of 'Splitter'
    # Break out of the loop if the 'Verifier' instance returns 'True' for the extracted list of sub-lists
    while True:
        matrix = []
        for _ in range(size):
            matrix.append(gen.generate(size))
        if check.verify(extract.split(matrix)):
            return matrix