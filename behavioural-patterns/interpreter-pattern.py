# Everything that a developer writes is interpreted by the computer!
# The Interpreter Design Pattern is all about processing textual input.
# For example: Turning text into object-oriented programming structures, programming language compilers,
# code interpreters and code analysis in integrated development environments (IDEs), Processing 
# HTML and XML by Browsers, evaluating numeric expressions, Regular Expressions etc.
# Interpreters turn text (strings) into OOP based structures in a complicated process.

# An Interpreter is a Component (class) that processes structured text data. It does so by turning the text
# into seperate lexical tokens (lexing) and then interpreting sequences of said tokens (parsing)   


# Barring simple cases, an Interpretor acts in two stages:
#   * Lexing turns text into a set of tokens
#   * Parsing tokens into meaningful constructs
# The parsed data can then be traversed, printed or evaluated!



# MATHEMATICAL EXPRESSIONS AS AN EXAMPLE OF INTERPRETER:


from enum import Enum, auto # For creating Enumerator

# A token is every single integer or operator in a mathematical expression
class Token:
    # Enumerator inside a class (Inner Class)
    class Type(Enum):
        # auto() automatically update the Enum index in ascending order
        INTEGER = auto()
        PLUS = auto()
        MINUS = auto()
        LPAREN = auto()
        RPAREN = auto()

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        return f'`{self.text}`' # The backticks are included in the string representation to visualize
        # leading and trailing whitespaces

def lex(input):
    result = []
    i = 0 # index of text string
    while (i < len(input)):
        if input[i] == '+':
            result.append(Token(Token.Type.PLUS, '+'))
        elif input[i] == '-':
            result.append(Token(Token.Type.MINUS, '-'))
        elif input[i] == '(':
            result.append(Token(Token.Type.LPAREN, '('))
        elif input[i] == ')':
            result.append(Token(Token.Type.RPAREN, ')'))
        else: 
            digits = [input[i]]
            # We donot know the number of digits in the integer, so we iterate till we encounter a non-digit
            for j in range(i+1, len(input)):
                if input[j].isdigit():
                    # keep appending to the digits of the encountered integer number as long as successive
                    # characters are also digits. When a non-digit character is encountered, create a
                    # token with the collected digits and append to the result. Then break out of the for loop.
                    digits.append(input[j])
                    i += 1 # increment index of the while loop as well, as long as successive digits are encountered
                else:
                    result.append(Token(Token.Type.INTEGER, ''.join(digits)))
                    break
        i += 1 # increment the while loop index as the index is not incremented when a non-digit character is encountered
    return result # list of tokens is returned



# Turn the sequence of tokens into an expression tree that can be subsequently traversed if required
# (like using Visitor Pattern)

class Integer: # Seperate class to store integers
    def __init__(self, value):
        self.value = value

# A class for a mathematical expression with two operends and an operator (such as addition and subtraction)
class BinaryExpression:
    class Type(Enum): # Enumerator (Inside Class)
        ADDITION = auto()
        SUBTRACTION = auto()

    def __init__(self):
        self.type = None
        self.left = None
        self.right = None
    
    @property
    def value(self): # the dynamically evaluated value of the expression
        # Remember that even if left and/or right are 'Integer' instances, they will have the 'value' attribute
        if self.type == self.Type.ADDITION:
            return self.left.value + self.right.value
        else: # or subtraction
            return self.left.value - self.right.value

def parse(tokens):
    result = BinaryExpression()
    have_lhs = False # At the start, the Binary Expression will not have a LHS
    i = 0
    while(i < len(tokens)):
        token = tokens[i]
        if token.type == Token.Type.INTEGER:
            integer = Integer(int(token.text))
            if not have_lhs: # If the LHS of the expression is not yet complete
                result.left = integer
                have_lhs = True
            else:
                result.right = integer
        # When a '+' Token is encountered, the 'BinaryExpression.type' becomes ADDITION
        elif token.type == Token.Type.PLUS:
            result.type = BinaryExpression.Type.ADDITION
        # When a '-' Token is encountered, the 'BinaryExpression.type' becomes SUBTRACTION
        elif token.type == Token.Type.MINUS:
            result.type = BinaryExpression.Type.SUBTRACTION 
        elif token.type == Token.Type.LPAREN:
            # If you encounter LPAREN, keep looping from this index till you reach a RPAREN
            # and use the Tokens inbetween these LPAREN token index and RPAREN token index to construct the
            # 'BinaryExpression' instance
            j = i 
            # increment the j index in a while loop till RPAREN token is encountered in the 'tokens'
            while (j < len(tokens)):
                if tokens[j].type == Token.Type.RPAREN:
                    break
                j += 1 # increment index 'j' by 1 because it will be the end index of list subsetting on 'tokens'.
                # The element in the end index of a subset operation will not be included in list subsetting
            subexpression = tokens[i+1:j]
            element = parse(subexpression) # RECURSIVE CALL TO CREATE RECURSIVE BINARY EXPRESSIONS
            if not have_lhs:
                result.left = element
                have_lhs = True
            else:
                result.right = element
            i = j # set the while loop index 'i' to the last index of the subexpression 'j' because we don't want
            # to go through the already processed tokens again!
        i += 1 # increment the while loop index 'i' by 1 for the next condition-checked iteration of the 
        # outer while loop
    return result


# Function to calculate the final value by evaluation an expression string
def calc(input):
    tokens = lex(input)
    print(' '.join(map(str, tokens))) # calls the __str__() method of every individual 'Token' instance
    # and combines with one whitespace character as delimiter

    parsed = parse(tokens) # Creates a Recursive BinaryExpression class / data-structure out off the tokens
    print(f'{input} = {parsed.value}') # Display the mathematical expression


if __name__ == '__main__':
    calc('(13+4)-(12+1)')





# EXERCISE:

# You are asked to write an expression processor for simple numeric expressions with the following constraints:
#   * Expressions use integral values (e.g., '13' ), single-letter variables defined in 'variables', as well as + 
#     and - operators only
#   * There is no need to support braces or any other operations
#   * If a variable is not found in 'variables' (or if we encounter a variable with > 1 letter, e.g. ab), the 
#     evaluator returns 0 (zero)
#   * In case of any parsing failure, evaluator returns 0

from enum import Enum

class Token:
    class Type(Enum):
        INTEGER = 0
        PLUS = 1 
        MINUS = 2
    def __init__(self, text, token_type):
        self.text = text
        self.token_type = token_type
    def __str__(self):
        return '`{}`'.format(self.text)
        
class ExpressionProcessor:
    def __init__(self):
        self.variables = {}

    def calculate(self, expression):
        tokens = []
        i = 0
        while (i < len(expression)):
            if expression[i] == '+':
                tokens.append(Token('+', Token.Type.PLUS))
            elif expression[i] == '-':
                tokens.append(Token('-', Token.Type.MINUS))
            elif expression[i].isdigit():
                digits = [expression[i]]
                for j in range(i+1, len(expression)):
                    if expression[j].isdigit():
                        digits.append(expression[j])
                    else:
                        i = j - 1
                        tokens.append(Token(''.join(digits), Token.Type.INTEGER))
                        break
            else:
                name = [expression[i]]
                for j in range(i+1, len(expression)):
                    if (expression[j] not in ['+', '-']) and (not expression[j].isdigit()):
                        name.append(expression[j])
                    else:
                        i = j - 1
                        if not ''.join(name) in self.variables:
                            return 0
                        else:
                            tokens.append(Token(self.variables[''.join(name)], Token.Type.INTEGER))
                        break
            
            i += 1
        value = int(tokens[0].text)
        i = 1
        while(i < len(tokens)):
            if tokens[i].Type == Token.Type.PLUS:
                value += int(tokens[i+1].text)
            elif tokens[i].Type == Token.Type.MINUS:
                value -= int(tokens[i+1].text)
            i += 2
        return value
    



# ALTERNATIVE APPROACH TO EXERCISE

import re
from enum import Enum

# Use a custom method to split the expression by 
def megasplit(pattern, string):
    # 'list((m.start(), m.end()) for m in re.finditer("(?<=[+-])", "1+23+456"))' will return:
    # [(2, 2), (5, 5)]
    splits = list((m.start(), m.end()) for m in re.finditer(pattern, string))
    starts = [0] + [i[1] for i in splits] # [0, 2, 5]
    ends = [i[0] for i in splits] + [len(string)] # [2, 5, 8]
    return [string[start:end] for start, end in zip(starts, ends)] # ['1+', '23+', '456']
    # Note that the operator itself is added as the last character because starts and ends contain
    # the "(?<=[+-])" pattern will return the start and end indices of the character before which there
    # was a match for [+-]

class ExpressionProcessor:
    class NextOp(Enum):
        PLUS = 1
        MINUS = 2

    def __init__(self):
        self.variables = {}

    def calculate(self, expression):
        current = 0
        next_op = None

        # doesn't work in python 3.5
        # parts = re.split('(?<=[+-])', expression)
        # The look-behind assertion '(?<=...)' matches if the current position in the string is preceded by 
        # a match for '...' that ends at the current position. 
        # For Example: re.finditer("(?<=[+-])", "1+23+456")) will return [(2, 2), (5, 5)] which are the positions
        # of the characters before which [+-] characters occur in the expression string. The 're.finditer()'
        # method returns match objects with start and end positions of the match which will be a same in this
        # case because only a single character will this pattern.
        parts = megasplit('(?<=[+-])', expression) # ['1+', '23+', '456']

        for part in parts:
            # split each element by the operator and extract just the integer (first element) part
            noop = re.split('[\+\-]', part)
            first = noop[0]
            value = 0

            try:
                value = int(first) # try converting to int
            except ValueError: # upon error in integer conversion, check if it is a key in 'self.variables'
                # also perform check on the length of the key to return zero if key length > 1
                if len(first) == 1 and first[0] in self.variables:
                    value = self.variables[first[0]]
                else:
                    return 0

            # According to the 'next_op' character, modify the 'current' result accumulator variable
            if not next_op:
                current = value
            elif next_op == self.NextOp.PLUS:
                current += value
            elif next_op == self.NextOp.MINUS:
                current -= value

            # Update the 'next_op' according to the end character in current 'part'
            if part.endswith('+'):
                next_op = self.NextOp.PLUS
            elif part.endswith('-'):
                next_op = self.NextOp.MINUS
            # for the last element in 'parts', there will be no operator character at the end.
            # we take care of this edge case here!
            else:
                next_op = None

        return current # return the final evaluation of the expression