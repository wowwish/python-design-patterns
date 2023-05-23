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
                # continue growing the integer if successive digits are encountered
                for j in range(i+1, len(expression)):
                    if expression[j].isdigit():
                        digits.append(expression[j])
                    # Stop at the index where a non-digit charecter is encountered and start the next
                    # iteration of the outer while loop from this character
                    else:
                        i = j - 1 # j - 1 is used here because i will be incremented at the end by 1
                        break
                tokens.append(Token(''.join(digits), Token.Type.INTEGER))
            else:
                name = [expression[i]]
                # continue growing the variable name if successive variable name characters are encountered
                for j in range(i+1, len(expression)):
                    if (expression[j] not in ['+', '-']) and (not expression[j].isdigit()):
                        name.append(expression[j])
                    # Stop at the index where a variable name ends and start the next
                    # iteration of the outer while loop from this character
                    else:
                        i = j - 1 # j - 1 is used here because i will be incremented at the end by 1
                        break
                # If length of the varable name is > 1, return 0. 
                # Otherwise, if variable name generated is in 'self.variables' dictionary, create an integer 
                # token with the corresponding value and add it to the list of tokens
                if len(name) > 1:
                    return 0
                elif ''.join(name) in self.variables:
                    tokens.append(Token(self.variables[''.join(name)], Token.Type.INTEGER))
                else:
                    # If the variable name is not in 'self.variables', return 0
                    return 0
            # increment the while loop index 'i'
            i += 1
        # set the value to be the first integer number in the expression
        value = int(tokens[0].text)
        i = 1
        while(i < len(tokens)):
            # iterate over the list of tokens from the second element by two steps in every iteration.
            # In each iteration, check the operation at the current index and modify 'value' accordingly
            # with the second operand of the operation (in the next index).
            if tokens[i].token_type == Token.Type.PLUS:
                value += int(tokens[i+1].text)
            elif tokens[i].token_type == Token.Type.MINUS:
                value -= int(tokens[i+1].text)
            i += 2 # We check two elements in 'tokens' in every iteration where the first element is the
            # operation token and the second element an integer token. Hence, we increment the index for
            # the next iteration by 2 
        return value
    
# ep = ExpressionProcessor()
# ep.variables['x'] = 5
# print(ep.calculate('1'))
# print(ep.calculate('1+2'))
# print(ep.calculate('1+x'))
# print(ep.calculate('1+xy'))






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
    

ep = ExpressionProcessor()
ep.variables['x'] = 5
print(ep.calculate('1'))
print(ep.calculate('1+2'))
print(ep.calculate('1+x'))
print(ep.calculate('1+xy'))