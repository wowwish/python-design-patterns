# The Flyweight Design Pattern is a Space Optimization Technique that tries to save Memory.
# This pattern tries to avoid redundancy by storing the data associated with similar objects externally
# and use indexes or references to this external data store. 

# For example: First and Last Names of plenty of Players of an MMORPG! It makes no sense to store the same
# first or last name over and over again. Instead, we can store a list of names and then store just the 
# references to names in the list instead of string copies of the names.
# You can also apply the notion of "ranges" to control properties of a set (successive) elements of a Homogenous 
# collection and store only the data related to the "ranges" instead of storing data corresponding
# to every element of the collection

import string
import random

# A function to generate a random 8 character string to be used as a name
def random_string():
    chars = string.ascii_lowercase
    return ''.join([random.choice(chars) for _ in range(8)])

class User:
    def __init__(self, name):
        self.name = name

# A class implementing the Flyweight Pattern to save up memory space
class User2:
    strings = [] # A static attribute (class variable) that stores all unique first and last names encountered
    # by the instances of this class during initantiation
    def __init__(self, full_name):
        # split the whole name into the first name and last name parts and simply store the indices of
        # the first name and last name into the
        def get_or_add(s): # A helper function
            # return the index of a string 's' within 'self.strings' which is a list of all the unique
            # first and last names. When 's' is not present in 'self.strings', add 's' 'self.strings' and
            # return the last index position in 'self.strings'
            if s in self.strings:
                return self.strings.index(s)
            else:
                self.strings.append(s)
                return len(self.strings) - 1
        self.names = [get_or_add(x) for x in full_name.split(' ')]
    
    # string representation of the user's name
    def __str__(self):
        return ' '.join([self.strings[x] for x in self.names])

# if __name__ == '__main__':
#     users = []
#     first_names = [random_string() for _ in range(100)]
#     last_names = [random_string() for _ in range(100)]
    # create cartesian product of first and last names and append to the 'users' list
    # Here, there are only 100 unique first names and 100 unique last names that produce 10,000 name 
    # combinations. This is where we can apply the Flyweight Pattern to reduce memory usage!
    # for first in first_names:
    #     for last in last_names:
            # users.append(User(f'{first} {last}'))
            # users.append(User2(f'{first} {last}')) # A huge memory saver - allocate 200 instead of 10,000 strings
    # print(users[0])





# Another example, is text formatting in a Text Editor. When you want to make chunks of the text bold or italic,
# you don't really want to take each individual character and give them an additional formatting flag. Instead,
# you can operate with ranges - (<line number:start>, <line number:end>) which specify the successive characters
# that should be bold or italicized.

class FormattedText:
    def __init__(self, plain_text):
        self.plain_text = plain_text
        # Brute force approach - use a Boolean Array of the same length of the input text to mark characters
        # that have to be formatted a particular way (capitalized or bold or italicized)
        # This creates a Boolean Array just as long as the input string!
        self.caps = [False] * len(plain_text)
    
    # method to set the values in the boolean array to True for characters which require capitalization
    def capitalize(self, start, end):
        for i in range(start - 1, end + 1):
            self.caps[i] = True

    # string representation of the formatted text
    def __str__(self):
        result = []
        for i in range(len(self.plain_text)):
            c = self.plain_text[i] # each individual character of the 'plain_text' string
            # capitalization is done for characters that require it by checking the Boolean Array 'caps'
            result.append(c.upper() if self.caps[i] else c)
        return ''.join(result)

# A class implementing the Flyweight pattern to save up space
class BetterFormattedText:
    def __init__(self, plain_text):
        self.plain_text = plain_text
        # Instead of creating a boolean array, we can use a list of ranges (start, end, type of formatting) 
        # which specify the indices of characters within the text that need particular formatting 
        # (bold, italicized, capitalized etc.)
        self.formatting = []
    
    # An inner class (a class inside another class) that gives the blueprint for a formatting range object
    class TextRange:
        # The text range will contain a start index, end index and a boolean value indicating whether
        # to capitalize or not
        def __init__(self, start, end, capitalize = False):
            self.start = start
            self.end = end
            self.capitalize = capitalize
        # method to check if a particular position in the text string is covered by this formatting range
        def covers(self, position):
            return self.start <= position <= self.end
    
    # method of the 'BetterFromattedText' class for creating a 'TextRange' instance out of the given
    # start and end index and set the default format of text in this range to be un-capitalized in 
    # 'self.plain_text'. Then, this range is 
    def get_range(self, start, end):
        # use 'self.TextRange()' to instantiate the 'TextRange' class with the 'start' and 'end' arguments
        range = self.TextRange(start - 1, end + 1)  
        # push the 'TextRange' instance into the list of text string index ranges that require formatting
        self.formatting.append(range)
        return range # The created 'TextRange' instance is also returned here. This is a reference to the
        # instance in 'self.formatting' and can be used to manipulate the format specifier 'self.capitalize'
        # of this 'TextRange' instance
    
    # string representation of the text with included formatting
    def __str__(self):
        result = []
        for i in range(len(self.plain_text)): # loop through every character in the text string
            c = self.plain_text[i]
            for r in self.formatting: # For every 'TextRange' instance in 'self.formatting'
                # if the 'TextRange' instance includes the position 'i' from 'self.plain_text' and the
                # range object specifies the font to be capitalized
                if r.covers(i) and r.capitalize:
                    c = c.upper()
                result.append(c) # append either the uppercase or normal string character as you loop through
                # the text string
        return ''.join(result)


if __name__ == '__main__':
    text = 'This is a brave new world'
    ft = FormattedText(text)
    ft.capitalize(11, 15)
    print(ft)
    # create an instance of the Flyweight Pattern class for the text string to save memory space
    bft = BetterFormattedText(text)
    # create a range object and set it to be capiralized when the 
    bft.get_range(17, 19).capitalize = True
    print(bft)




# EXERCISE

# You are given a class called 'Sentence' , which takes a string such as "hello world". 
# You need to provide an interface such that the indexer returns a flyweight that can be used to 
# capitalize a particular word in the sentence.

class Sentence:
    class WordToken:
        def __init__(self, capitalize=False):
            self.capitalize = capitalize

    def __init__(self, plain_text):
        self.words = plain_text.split(' ')
        self.tokens = [self.WordToken() for w in self.words]
    # method to get out the 'WordToken' instance at the given index in 'self.tokens'
    def __getitem__(self, item):
        return self.tokens[item]
    def __str__(self):
        result = []
        for i in range(len(self.words)):
            w = self.words[i]
            if self.tokens[i].capitalize:
                w = w.upper()
            result.append(w)
        return ' '.join(result)
    

s = Sentence('alpha beta gamma')
s[1].capitalize = True
print(s)