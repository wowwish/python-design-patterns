# The Mememto Design Pattern is used to cache an object's "state" to return to that "state" later.
# An object or system will go through several changes. For example, a bank account gets deposits and 
# withdrawals. There are different ways of navigating through these changes (transitioning).
# One way is to record every change (model a change as a command that can also 'undo' itself, similar
# to what we saw in the Command Pattern!).
# Another simpler approach is to simply save snapshots of the system at different points - a Memento,
# that allows us to restore the system (object) back to its "state" contained in the Mememto.

# A Memento is a token/handle class representing the system (object) "state". It lets us roll back to the
# "state" when the Memento was generated. A Mmemnto may or may not directly expose its cached "state" 
# information of the system (or object).
# Mementos can be used to rollback to "states" arbitrarily. A Memento typically has no functions of
# its own! Also, similar to the Command Pattern, Memento can be used to implement undo / redo operations!

# You can also store every single "state" of the system as a Memento instance and use this to implement
# undo/redo functionality, but this requires too much memory.

# A Memento class that can be instantiated to save the state of a 'BankAccount' instance
class Memento:
    def __init__(self, balance):
        self.balance = balance
        

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        # A list to store snapshots before every change in the "state" of the system
        self.changes = [Memento(self.balance)]
        self.current = 0 # index of the current (latest) Memento instance in the list of Memento snapshots
    def deposit(self, amount):
        self.balance += amount
        m = Memento(self.balance)
        self.changes.append(m)
        self.current += 1
        return m
    # method to restore the "state" of an instance of this class to the "state" preserved in 
    # the given Memento
    def restore(self, memento):
        # memento can be 'None' because 
        if memento:
            self.balance = memento.balance
            # after restoring the system, add the Memento with the cached "state" to which we restored
            # the system, to the growing list in 
            self.changes.append(memento) # index to store the latest 
            self.current = len(self.changes) - 1
    def undo(self):
        if self.current > 0:
            self.current -= 1
            # To undo the last (most recent) "state" change, simply restore to the "state" from the
            # most recently cached (current) Memento instance in 'self.changes'
            m = self.changes[self.current]
            self.balance = m.balance
            return m
        return None # If there are no current Momento instances in 'self.changes', 'self.current' will
        # be 0 and so, we return 'None' in this situation
    def redo(self):
        # We cannot redo when we are currently at the latest "state" of the system
        if self.current + 1 < len(self.changes):
            self.current += 1
            m = self.changes[self.current]
            self.balance = m.balance
            return m
        return None # When we are already at the latest "state" of the system, there is no undone
        # operation to redo. Hence we return 'None' in this scenario
    def __str__(self):
        return f'Balance = {self.balance}'

if __name__ == '__main__':
    ba = BankAccount(100) # We currently don't have a Memento instance for the initial state of 
    # the 'BankAccount' instance 'ba'
    # m1 = ba.deposit(50) # caching "state" of 'ba' in a Memento instance 'm1'
    # m2 = ba.deposit(25) # caching "state" of 'ba' in a Mememnto instance 'm2'
    # print(ba)
    # ba.restore(m1) # restore to the "state" stored in 'm1'
    # print(ba)
    ba.deposit(50)
    ba.deposit(25)
    print(ba)
    ba.undo()
    print(f'Undo 1 : {ba}')
    ba.undo()
    print(f'Undo 2 : {ba}')
    ba.redo()
    print(f'Redo: {ba}')




# EXERCISE 


# A 'TokenMachine' is in charge of keeping tokens. Each 'Token' instance is a reference type with a 
# single numerical value. The machine supports adding tokens and, when it does, it returns a memento 
# representing the state of that system at that given time.
# You are asked to fill in the gaps and implement the Memento design pattern for this scenario. 
# Pay close attention to the situation where a token is fed in as a reference and its value is 
# subsequently changed on that reference - you still need to return the correct system snapshot!


from copy import deepcopy # To create Memento instances using clones of 'self.tokens' instead of 
# using references to 'self.tokens' to create Memento instances

class Token:
    def __init__(self, value=0):
        self.value = value

class Memento(list):
    pass

class TokenMachine:
    def __init__(self):
        self.tokens = []

    def add_token_value(self, value):
        return self.add_token(Token(value))

    def add_token(self, token):
        self.tokens.append(token)
        # we perform deepcopy here to prevent using references as 'self.tokens' can change
        # over time and a reference to this will lead to wrong "state" information
        m = Memento(deepcopy(self.tokens))
        return m

    def revert(self, memento):
        # again, to prevent references, we take every token from the "state" stored in the Memento
        # instance and make it into a list and store it in 'self.tokens'
        self.tokens = [token for token in memento]