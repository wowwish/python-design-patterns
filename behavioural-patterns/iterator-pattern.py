# The Iterator Design Pattern is used for the traversal (iteration) which is a core functionality 
# of various Data Structures. An Iterator is a class that facilitates the traversal through a data structure.
# The Iterator keeps a reference to the current element and knows how to move to a different element.

# The Iterator protocol requires an __iter__() method to expose the Iterator, and a __next__() method which 
# returns each of the elements that are iterated over or traversed. The __next__() method will raise 
# 'StopIteration' when it no longer has elements to iterate over or traverse

# A stateful Iterator (An Iterator that can keep track of which elements have been already traversed/visited
# using internal state (attributes) cannot be recursive). They also cannot pause/resume providing elements in 
# the middle of runtime. Hence, Generators which utilize the 'yield' keyword of python are allow for building
# much more succinct Iterators in python!


# ITERATOR OF A BINARY TREE

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = None # By default, the Node instance (Root) is not connected to a parent node in the tree

        if left:
            # The parent of the left sub-Node if it is not None, is this Node itself
            self.left.parent = self 
        if right:
            # similarly, the parent of the right sub-Node if it is not None, is this Node itself
            self.right.parent = self
    
    # Method to create an Iterator object for this Binary Tree, that returns each Node instance of the tree
    # in a particular order by invoking the __next__() method internally (within the Iterator).
    # At many instances, we get a need to access an object like an iterator. One way is to form a generator 
    # loop but that extends the task and time taken by the programmer. Python eases this task by providing a 
    # built-in method __iter__() for this task.
    # The __iter__() function returns an iterator for the given object (array, set, tuple, etc. or custom objects). 
    # It creates an object that can be accessed one element at a time using __next__() function, which generally 
    # comes in handy when dealing with loops.
    def __iter__(self): # magic method overriding
        return InOrderIterator(self)


# An Iterator to traverse the Binary Tree In-Order (left sub-tree first, then root, then right sub-tree)
class InOrderIterator:
    def __init__(self, root):
        self.root = self.current = root # the root and the current element are initialized as the same Node
        self.yielded_start = False # flag to keep track of whether the first element in traversal has been visited
        # first element for in-order traversal: iteratively traverse to the left-most leaf (terminal) node 
        # of the tree and set this node as 'self.current', the first element that will be returned
        # by __next__().
        while self.current.left:
            self.current = self.current.left
    # At many instances, we get a need to access an object like an iterator. One way is to form a generator 
    # loop but that extends the task and time taken by the programmer. Python eases this task by providing a 
    # built-in method __iter__() for this task.
    # The __iter__() function returns an iterator for the given object (array, set, tuple, etc. or custom objects). 
    # It creates an object that can be accessed one element at a time using __next__() function, which generally 
    # comes in handy when dealing with loops.
    def __next__(self): # method to move from one element to another
        # If the first element according to the order of traversal (the leftmost terminal sub-tree in the case
        # of in-order traversal) has not been visited/traversed yet (the 'yielded_start' flag is False), then
        # return that 
        if not self.yielded_start:
            self.yielded_start = True
            return self.current
        
        # Otherwise, if 'self.right' exists, then visit/traverse that right sub-tree once and from there, we
        # traverse the right sub-tree to the last unvisited left sub-tree of the right-sub-tree node of 
        # 'self.current' and return that.  
        if self.current.right:
            self.current = self.current.right
            # recursively move to the left-most terminal 
            while self.current.left:
                self.current = self.current.left
            return self.current
        # If the first element according to order of traversal has been visited/traversed and 'self.current.right'
        # does not exist, then we move to one level above (the parrent of the current Node). 
        else:
            p = self.current.parent
            # keep iteratively checking if the lst visited node is the right sub-tree of its parent node, 
            # while iteratively setting the parent Node to the parent of current node (bubbling-up). Finally,
            # set 'self.current' to the parent Node 'p' where (the last visited node)) 'self.current' is NOT 
            # THE RIGHT SUB-TREE (in other words, traverse up to the parent Node whose left sub-tree contains the
            # set of all currently traversed/visited Nodes of the Binary Tree). 
            # This condition block ensures that move from left sub-tree to current value
            # to right sub-tree at every Node instance in the Binary Tree (maitaining the in-order traversal)
            while p and self.current == p.right:
                self.current = p
                p = p.parent
            self.current = p
            # if self.current exists after bubbling-up (non Root node), then we return 'self.current'
            if self.current:
                return self.current
            # otherwise, we terminate the Iterator (Root node has no parent)
            else:
                raise StopIteration


# A Nested Generator function to perform in-order traversal of a Binary Tree. When the Iterator is implemented
# in the form of a Generator function like this, the state of the Iterator is managed implicitly unlike our
# previous class-based implementation!
def traverse_in_order(root):
  def traverse(current):
    if current.left:
      for left in traverse(current.left): # Recursion used to traverse left sub-tree
        yield left
    # The 'yield' statement can restart from where it is left off and can also be called multiple times
    # unlike the 'return' statement 
    yield current # yield the current Node after yielding all the nodes of the left sub-tree
    if current.right:
      for right in traverse(current.right): # Recursion used to traverse right sub-tree
        yield right
  for node in traverse(root): # yield results from the inner Generator function
    yield node
                




if __name__ == '__main__':
    #    1
    #  /   \
    # 2     3

    # in-order: 213
    # preorder: 123
    # postorder: 231

    root = Node(1, Node(2), Node(3)) # Binary tree with root node, left and right sub-trees
    # create an InOrderIterator instance that starts from the root node of the binary tree 'root'
    it = iter(root) # The iter() method implicitly calls the __iter__() method and returns an Iterator for the 
    # given argument and in this case, it returns an in-order traversing iterator due to method overriding
    print([next(it).value for x in range(3)]) # print the first three elements from the in-order Iterator for
    # the binary tree 'root'

    # We can also use the InOrderIterator instance implicitly using a for loop
    for x in root:
       print(x.value)
    
    for y in traverse_in_order(root):
        print(y.value)




# ALTERNATIVE IMPLEMENTATION OF ITERATOR

# Take the example of iterating over the stats of a creature in a game


class Creature:
    # hard-code the index of particular statistic of the creature in the list 'self.stats'
    # A better approach is to use a dictionary instead of a list for 'self.stats'
    _strength = 0
    _agility = 1
    _intelligence = 2

    # constructor
    def __init__(self, stats):
        # self.strength = 10
        # self.agility = 10
        # self.intelligence = 10
        self.stats = [10, 10, 10]

    # imageine you have a property to collect the sum of all the stat values of the creature. Everytime
    # a new type of stat is added (say, something like defense or attack), you have to remember to
    # modify the formula for this property as well! Similarly, you would need to modify all other properties
    # that depend upon the maximum stat or the number of stats etc.
    # THIS MAKES THE CODE UGLY!
    # To rectify this, one approach we can follow is to store the stats of the creature in a list
    
    @ property
    def strength(self):
       return self.stats[Creature._strength] # Access class attributes with the class name always!

    @strength.setter
    def strength(self, value):
       self.stats[Creature._strength] = value # Access class attributes with the class name always!
    
    @ property
    def agility(self):
       return self.stats[Creature._agility] # Access class attributes with the class name always!

    @agility.setter
    def agility(self, value):
       self.stats[Creature._agility] = value # Access class attributes with the class name always!  
    
    @ property
    def intelligence(self):
       return self.stats[Creature._intell] # Access class attributes with the class name always!

    @intelligence.setter
    def intelligence(self, value):
       self.stats[Creature._intelligence] = value # Access class attributes with the class name always!

    @property
    def sum_of_stats(self):
        # return self.strength + self.intelligence + self.agility
        return sum(self.stats)
    
    @property
    def max_stat(self):
        # return max(self.strength, self.intelligence, self.agility)
        return max(self.stats)
    
    @property
    def average_stat(self):
        # return self.sum_of_stats / 3.0
        return float(self.sum_of_stats) / len(self.stats)





# EXERCISE

# Given the following definition of a 'Node' , please implement preorder traversal right inside 'Node'.
# in Pre-Order traversal, the root node is traversed/visited first, then the left sub-tree, 
# then the right sub-tree.
# The sequence returned should be the sequence of values, not their containing nodes.

class Node:
    def __init__(self, value, left=None, right=None):
        self.right = right
        self.left = left
        self.value = value
    
        self.parent = None

        if left:
            self.left.parent = self
        if right:
            self.right.parent = self
        
    def traverse_preorder(self):
        yield self.value
        # Recursion on left sub-tree
        if self.left: # if the left sub-tree exists for the current 'Node' instance then recursively apply
            # the pre-order traversal to it
            # What yield from does is it establishes a transparent bidirectional connection between the caller 
            # and the sub-generator:
            #  * The connection is "transparent" in the sense that it will propagate everything correctly too, 
            #    not just the elements being generated (e.g. exceptions are propagated).
            #  * The connection is "bidirectional" in the sense that data can be both sent from and to the
            #    sub-generator (by using  'w = (yield)' in the sub-generator declaration, the sub-generator 
            #    can get data from outside and simply yield it or manipulate it internally. Similarly, you
            #    can send data from outside to a sub-generator using the 'generator.send()' method which will
            #    be taken and stored in the variable 'w' if the sub-generator has the 'w = (yield)' statement
            #    to take in external data).
            yield from self.left.traverse_preorder() # yield from a sub-Generator from the recursive call
        # recursion on right sub-tree
        if self.right: # if the right sub-tree exists for the current 'Node' instance then recursively apply
            # the pre-order traversal to it
            # What yield from does is it establishes a transparent bidirectional connection between the caller 
            # and the sub-generator:
            #  * The connection is "transparent" in the sense that it will propagate everything correctly too, 
            #    not just the elements being generated (e.g. exceptions are propagated).
            #  * The connection is "bidirectional" in the sense that data can be both sent from and to the
            #    sub-generator (by using  'w = (yield)' in the sub-generator declaration, the sub-generator 
            #    can get data from outside and simply yield it or manipulate it internally. Similarly, you
            #    can send data from outside to a sub-generator using the 'generator.send()' method which will
            #    be taken and stored in the variable 'w' if the sub-generator has the 'w = (yield)' statement
            #    to take in external data).
            yield from self.right.traverse_preorder() # yield from a sub-Generator from the recursive call
    
