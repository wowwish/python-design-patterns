# Consider an ordinary telephone. What you can do with the telephone depends on the "state" of its phone/line
#   * If the phone is ringing or if you want to make a call, you can pick up the phone
#   * The phone also has to be off the hook to actually recieve a call or make a call
#   * If you call someone and the line is busy, you can put the handset down.

# Changes in "state" can be explicit, or in response to an event (AS SEEN IN THE OBSERVER PATTERN)

# The State Design Pattern is a Pattern in which an object's behaviour is determined by its state. An object
# transitions from one state to another (something needs to trigger this "transition").
# A formalized construct which manages "state" and "transition" is called a "state machine".

# Given sufficient complexity, it pays to formally define possible "states".
# and events/triggers. We can also define the "state" entry/exit behaviours
# and the actions that are driven by a particular "state" transition due
# to an event. Guard conditions for enabling/disabling particular "state" 
# transitions can also be set up. You can also have default actions for
# cases where no transition happens for an event.



# CLASSIC IMPLEMENTATION OF A STATE MACHINE

# Consider a Light Switch which can be On/Off

from abc import ABC # for creating abstract base classes

# This is a class which has a "state" associated with it
class Switch:
    def __init__(self):
        self.state = OffState()
    
    # we model the possible "states" that this switch can be in using classes and implement methods
    # that can modify the "state" of an instance of this class using transitioning methods implement
    # in the "state" model claees. 
    def on(self):
        self.state.on(self)

    def off(self):
        self.state.off(self)

# Abstract class to model a "state" of the 'Switch' class instances. Keep in mind that it is not 
# neccessary for abstract Classes to have any abstract methods in Python.
class State(ABC):
    def on(self, switch):
        print('Light is already on')

    def off(self, switch):
        print('Light is already off')

# State class model for the "on" state of 'Switch' instance. A better way to model the "state" would be
# to simply use an Enum instead of a class. Here, the "state" itself regulates the transition to another
# "state".
class OnState(State):
    def __init__(self):
        print('Light turned on')
    # method to transition from the "on" state to "off" state
    def off(self, switch):
        print('Turning light off...')
        switch.state = OffState()

# State class model for the "off" state of 'Switch' instance. A better way to model the "state" would be
# to simply use an Enum instead of a class. Here, the "state" itself regulates the transition to another
# "state".
class OffState(State):
    def __init__(self):
        print('Light turned off')
    # method to transition from the "off" state to "on" state
    def on(self, switch):
        print('Turning light on...')
        switch.state = OnState()


# if __name__ == '__main__':
#     sw = Switch()
#     sw.on()
#     sw.off()
#     sw.off() 
    # When the light is in 'OffState' and we call off(), 'State.Off()' is called since 'OffState'
    # does not have an implementation for the off() method (The Base Class "state" implementation is used)



# REALISTIC IMPLEMENTATION OF A STATE MACHINE

# Modelling a Phone Call

from enum import Enum, auto # For implementing Enumerator Classes

# The "States" of a Phone
class State(Enum):
    OFF_HOOK = auto() # When the Phone's reciever is off the hook
    CONNECTING = auto() # When the Phone is calling some number
    CONNECTED = auto() # When the Phone is on call
    ON_HOLD = auto() # When the Phone call is on hold
    ON_HOOK = auto() # When the Phone's reciever is on on the hook

# Triggers force transition of the Phone from one "State" to another
class Trigger(Enum):
    CALL_DIALED = auto() # A person is called
    HUNG_UP = auto() # A call was hung up by either party
    CALL_CONNECTED = auto() # A called person answers the call
    PLACED_ON_HOLD = auto() # An ongoing call is placed on hold by either party
    TAKEN_OFF_HOLD = auto() # An ongoing call is taken off hold
    LEFT_MESSAGE = auto() # The owner of the called number has left an
    # automated voice mail reply



# if __name__ == '__main__':
#     # A large map of rules for which transition (through Triggers) causes
#     # what changes in "State" of the Phone. These set of rules orchestrate
#     # the State Machine (get it to run or execute)
#     rules = {
#         # The keys of this dictionary correspond to different "States"
#         # of the Phone and the corresponding value is a list of 
#         # Trigger - new "State" tuple pairs with possible Triggers and
#         # the corresponding States that these Triggers put the Phone in.
#         State.OFF_HOOK: [(Trigger.CALL_DIALED, State.CONNECTING)],
#         State.CONNECTING: [(Trigger.CALL_CONNECTED, State.CONNECTED)],
#         State.CONNECTED: [(Trigger.LEFT_MESSAGE, State.ON_HOOK),
#                           (Trigger.HUNG_UP, State.ON_HOOK),
#                           (Trigger.PLACED_ON_HOLD, State.ON_HOLD)],
#         State.ON_HOLD: [(Trigger.TAKEN_OFF_HOLD, State.CONNECTED),
#                         (Trigger.HUNG_UP, State.ON_HOOK)]
#     }

#     state = State.OFF_HOOK
#     exit_state = State.ON_HOOK
#     # start with 'state' and loop until the 'state' != 'exit_state'
#     while state != exit_state:
#         # print the current Phone "State"
#         print(f'The phone is currently {state}')
#         # Print all available transition Triggers for the Phone's 
#         # current "State"
#         for i in range(len(rules[state])):
#             t = rules[state][i][0] 
#             print(f'{i} : {t}')
#         # Obtain the trigger as input from the user in the form of the
#         # list index of the trigger for the current Phone "State"
#         idx = int(input('Select a trigger: '))
#         # set the new "State" of the Phone to the transitioned "State"
#         s = rules[state][i][1]
#         state = s
#     print('\n\nWe are done using the Phone!!!!!')




# SWITCH-BASED STATE MACHINE EXAMPLE USING A NUMERIC COMBINATION LOCK

# The Switch-based state machine does not use any data-structure to 
# store the rules for the transitions. However, it tends to be more
# difficult to understand and unorganized because it implements the
# the rules as if-else-if conditions.

class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()

if __name__ == '__main__':
    code = '1234' # Passcode to unlock a combination lock
    state = State.LOCKED
    entry = ''

    while True: # Infinite Loop
        if state == State.LOCKED:
            entry += input(entry) # append user-input to the overall code
            if entry == code: 
                # If the currently collected code is the same as the passcode
                state = State.UNLOCKED
            if not code.startswith(entry):
                # if the currently collected code is not a prefix of the
                # actual passcode, set the state as failed
                state = state.FAILED
        elif state == State.FAILED:
            # reset for failed attempt
            print('\nFAILED!')
            entry = ''
            state = State.LOCKED
        elif state == state.UNLOCKED:
            # exit the infinite loop when the lock has been unlocked
            print('\nUNLOCKED!')
            break






# EXERCISE


# A combination lock is a lock that opens after the right digits have 
# been entered. A lock is preprogrammed with a combination (e.g., 12345 ) 
# and the user is expected to enter this combination to unlock the lock.
# The lock has a Status field that indicates the state of the lock. The 
# rules are:
#   * If the lock has just been locked (or at startup), the status is LOCKED.
#   * If a digit has been entered, that digit is shown on the screen. 
#   * As the user enters more digits, they are added to Status.
#   * If the user has entered the correct sequence of digits, the lock 
#     status changes to OPEN.
#   * If the user enters an incorrect sequence of digits, the lock status 
#     changes to ERROR.
# Please implement the 'CombinationLock' class to enable this behavior. 
# Be sure to test both correct and incorrect inputs.


class CombinationLock:
    def __init__(self, combination):
        self.combination = combination
        self.reset()

    def reset(self):
        self.status = 'LOCKED'
        self.digits_entered = 0
        self.failed = False

    def enter_digit(self, digit):
        if self.status == 'LOCKED':
            self.status = ''
        self.status += str(digit)
        if self.combination[self.digits_entered] != digit:
            self.failed = True
        self.digits_entered += 1

        if self.digits_entered == len(self.combination):
            self.status = 'ERROR' if self.failed else 'OPEN'




# ALTERNATIVE APPROACH

class CombinationLock:
    def __init__(self, combination):
        self.status = 'LOCKED'
        self.combination = ''.join([str(n) for n in combination])
    def reset(self):
        self.status = 'LOCKED'
    def enter_digit(self, digit):
        print(digit)
        if self.status == 'LOCKED':
            self.status = str(digit)
        else:
            self.status += str(digit)
            if not self.combination.startswith(self.status):
                self.status = 'ERROR'
            if self.combination == self.status:
                self.status = 'OPEN'

