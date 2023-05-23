# Ordinary statements such as variable assignment (x = 2) are "preishable" (you cannot undo the assignment 
# operation or rollback) and go back to the previous state. 
# You also cannot "Serialize" (save to a file or database) a sequence of actions (function calls)

# We want an object to process an operation and record the sequence of the operation for potential rollback
# This is achieved by the Command Design Pattern. The Command Pattern is used in GUI Commands (copy/paste), 
# multi-level undo/redo (Ctrl + Z, Ctrl + Y), macro recording and more!

# A Command is an object which represents an instruction to perform a particular action. It contains 
# (encapsulates) all the information necessary for the action to be taken (optionally, also to rollback
# the action!). The instruction for applying the command can be defined in the command itself or elswhere.
# Similarly, the instructions for undoing a command can also be defined. You can also use the Composite
# Pattern to create a sequence of commands to be processed one after another that behave as one command (macros)!


class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'Deposited {amount}, balance = {self.balance}')

    def withdraw(self, amount):
        # only withdraw amount when the balance after withdrawal wll be more than the overdraft limit
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f'Withdrew {amount}, balance = {self.balance}')
            return True # If the withdrawal was successful, return True 
        return False # If withdrawal was a failure due to lack of funds, return False
        
    def __str__(self):
        return f'Balance = {self.balance}'
    

# A Command - Interface for calling the methods of a 'BankAccount' instance. Also implements the recording
# (audit log) and undo functionalities.

from abc import ABC # for defining abstract classes
from enum import Enum # for Enumerators

# Define an Interface/Abstract class for the Command Pattern component
class Command(ABC):
    def __init__(self):
        self.success = None # A flag to keep track of whether the invoked command succeeded
    # a method to perform the action of the command
    def invoke(self): # you can also override the in-built __call__() method to perform same underlying logic
        pass
    # a method to revoke the action performed by the command
    def undo(self):
        pass

# A class that implements the Command Prototype
class BankAccountCommand(Command):
    # A class inside a class (inner-class) that is also an Enumerator
    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1
    def __init__(self, account, action, amount):
        super().__init__() # initialize with the 'Command' class constructor to add the 'self.success' attribute
        self.account = account
        self.action = action
        self.amount = amount
        
    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True # A deposit will always succeed
        elif self.action == self.Action.WITHDRAW:
            # capture the success/failure information for the withdrawal operation
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        # Only rollback changes when the command invoked actually succeeded!
        if not self.success:
            return
        # strictly speaking this is not correct
        # (you don't undo a deposit by withdrawing)
        # but it works for this demo, so...
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)


# DEPOSITING AND WITHDRAWING ACROSS BANK ACCOUNTS

# Use the Composite pattern to build a collection of commands that are masqueraded as a single command
class CompositeBankAccountCommand(Command, list):
    # CompositeBankAccountCommand's method-resolution-order is 'Command' and then 'list'.
    # Since both the 'Command' class and 'list' class '__init__()' methods donot require any arguments to 
    # be passed, the 'super().__init__()' calls the 'Command.__init__()' first and then 'list__init__()'
    # to add the 'self.success' attribute and to make this class into a collection 
    def __init__(self, items=[]):
        super().__init__() # initialize with 'list.__init__()'
        for i in items:
            self.append(i) # add all 'BankAccountCommand' instances from 'items' into 'self' since
            # this class inherits the 'list' class
    def invoke(self):
        for i in self:
            i.invoke()
    def undo(self):
        # The reversed() method computes the reverse of a given collection and returns it in the form of a list.
        for i in reversed(self): # undo should happen in reverse order - the last command invoked should
            # be rolled back first
            i.undo()

# We can tie up multiple commands to depend on the success status of one-another by implementing them
# as a seperate Composite class!
class MoneyTransferCommand(CompositeBankAccountCommand):
    def __init__(self, from_acc, to_acc, amount):
        # initializing the 'CompositeBankAccountCommand' constructor with the list of commands to be 
        # performed in order
        super().__init__([BankAccountCommand(from_acc, BankAccountCommand.Action.WITHDRAW, amount),
                          BankAccountCommand(to_acc, BankAccountCommand.Action.DEPOSIT, amount)]) 
        
    # override the inherited 'invoke()' method of 'CompositeBankAccountCommand' class to link the commands
    # in such a way that successive commands are invoked only when the previous command was a success
    def invoke(self):
        # flag to keep track of whether the previous command from the composite command collection
        # ran successfully
        ok = True
        for cmd in self:
            if ok: # If the last command was a success
                cmd.invoke()
                ok = cmd.success # set 'ok' to the success of the current command that was invoked
            else:
                cmd.success = False # something failed for the control flow to reach here, so set 
                # 'cmd.success' to False
        self.success = ok # The 'ok' flag keeps track of the the status of every command invocation. Successive
        # commands are invoked only when it stays 'True'. Hence, it reflects the success of the entire 
        # transaction command itself!

import unittest

class TestSuite(unittest.TestCase):
    # def test_composite_deposit(self):
    #     ba = BankAccount()
    #     deposit1 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
    #     deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 50)
    #     composite = CompositeBankAccountCommand([deposit1, deposit2])
    #     composite.invoke()
    #     print(ba)
    #     composite.undo()
    #     print(ba)
    
    # def test_transfer_fail(self):
    #     ba1 = BankAccount(100)
    #     ba2 = BankAccount()
    #     amount = 1000
    #     wc = BankAccountCommand(ba1, BankAccountCommand.Action.WITHDRAW, amount)
    #     dc = BankAccountCommand(ba2, BankAccountCommand.Action.DEPOSIT, amount)
    #     transfer = CompositeBankAccountCommand([wc, dc])
    #     # The first withdrawal of $1000 from 'ba1' fails because of overdraft limit.
    #     # The second deposit command of 'ba2' however, succeeds because it does not depend on the success of the
    #     # previous withdrawal command.
    #     transfer.invoke()
    #     print(f'ba1: {ba1}, ba2: {ba2}')
    #     # rolling back the deposit command in 'ba2' succeeds because the balance after removal falls within 
    #     # the overdraft limit
    #     # However, rolling back the withdrawal from 'ba1' does not happen because it failed when the command
    #     # was invoked!
    #     transfer.undo()
    #     print(f'ba1: {ba1}, ba2: {ba2}')
    
    def test_better_transfer(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()
        amount = 100
        transfer = MoneyTransferCommand(ba1, ba2, amount)
        transfer.invoke()
        print(f'ba1: {ba1}, ba2: {ba2}')
        transfer.undo()
        print(f'ba1: {ba1}, ba2: {ba2}')
        print(transfer.success)

if __name__ == '__main__':
    # ba = BankAccount() # create an empty bank account
    # cmd = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
    # cmd.invoke()
    # print(f'After $100 deposit: {ba}')

    # cmd.undo()
    # print(f'$100 deposit undone: {ba}')

    # A command that is not supposed to work is run. The 'illegal_cmd.invoke()' does not modify 
    # the BankAccount instance 'ba' because the bank account has 0 balanace and nothing can be withdrawn.
    # However, when we use 'illegal_cmd.undo()', we see that the rollover operation for the invoked command has 
    # happenend (Deposit of $1000 even though $1000 withdrawal was not successful when the command was invoked) 
    # even though the command actually failed! 
    # This is taken care by using 'self.success' flag in the 'BankAccountCommand' class
    # illegal_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 1000)
    # illegal_cmd.invoke()
    # print(f'After impossible withdrawal: {ba}')
    # illegal_cmd.undo()
    # print(f'After undo: {ba}')

    unittest.main()





# EXERCISE


# Implement the 'Account.process()' method to process different account commands.
# The rules are obvious:
#   * success indicates whether the operation was successful
#   * You can only withdraw money if you have enough in your account


from enum import Enum

class Command:
    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(self, action, amount):
        self.action = action
        self.amount = amount
        self.success = False
        
        
class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def process(self, command):
        if command.action == Command.Action.DEPOSIT:
            self.balance += command.amount
            command.success = True
        elif command.action == Command.Action.WITHDRAW:
            if self.balance >= command.amount:
                self.balance -= command.amount
                command.success = True
            else:
                command.success = False



