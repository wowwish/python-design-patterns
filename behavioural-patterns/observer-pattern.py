# The Observer Design Pattern to used to inform a system when a certain thing happens in the system. The
# different events that can trigger an Observer to inform the system include:
#   * Object's property changes
#   * Object does something (action)
#   * Some external event occurs
# The Observer Pattern listens for particular events in the system and notifies with useful information
# when such events occur. An Observer allows subscription to or unsubscription from such event triggered
# notifications

# An Observer is an object that wishes to be informed about events happening in the system. The entity
# generating the events is an "observable".
# An event is something that happens and needs a notification in the system when it happens.
# Consider a patient falling ill as an event to a doctor:

# The Observer Pattern is an Intrusive approach (you will have to modify a class): an "observable" must provide
# an "event" (modelled in our case as a list of function references) to subscribe to. 
# Subscription and Unsubscription can be handled with the addition/removal of items (handler functions for 
# an event) in a list.
# Property notifications are easy; dependent property (properties that depend on other properties of the class) 
# notifications are tricky.  


# EVENT OBSERVERS


# This 'Event' class is essentially a list of functions that need to be invoked when a particular event
# happens in the system, to make modifications in the system or to notify components of the system
# This 'Event' class is an Observer. It calls every function assigned to its list with all the arguments passed
# to it. Hence, instances can append their event handling functions to this list and have the 'Event' occurrence
# handled for them
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self: # Call all the functions (subscribers) of this particular Event Observer
            item(*args, **kwargs)



class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        # Create a new Observer to notify when this person falls ill
        self.falls_ill = Event() # now this instance has created an Event to which other outside
        # classes can subscribe to by adding their event handling functions to this list.

    def catch_a_cold(self):
        self.falls_ill(self.name, self.address) # We are calling the 'Event' Observer instance which fires
        # all the functions within its list

# A general function to create a notification about a person falling ill and requiring a doctor. This general
# function is utilized by appending it to a person's Event notification list (Observer).
def call_doctor(name, address):
    print(f'{name} needs a doctor at {address}')


# if __name__ == '__main__':
#     person = Person('Sherlock', '221B Baker St')
#     # We can either provide pre-defined function to the Event Observer or use lambda functions as well
#     person.falls_ill.append(lambda name, address: print(f'{name} is ill')) 
#     person.falls_ill.append(call_doctor) # we add the call_Doctor function to the Event Observer of this
#     # 'Person' instance
#     person.catch_a_cold() # This method fires off the Event Observer of 'person'

#     person.falls_ill.remove(call_doctor) # Unsubscribing 'person' from the Event Observer
#     person.catch_a_cold() # This method fires off the Event Observer of 'person'



# PROPERTY OBSERVERS - notifies when a property is changed for an object

# WHILE THESE PROPERTY OBSERVERS CAN BE USED TO REACT TO CHANGES IS A HANDFUL OF PROPERTIES, THEY ARE 
# INEFFECTIVE AND INSUFFICIENT FOR LARGE SCALE SYSTEM WHERE A LARGE NUMBER OF PROPERTIES HAVE TO BE 
# MONITORED. AN EXAMPLE WHERE THESE PROPERTY OBSERVERS WILL BE INSUFFICIENT IS IN AN EXCEL SHEET WHERE THE
# VALUE OF CELLS DEPEND ON VALUES OF OTHER CELLS AND REACT TO CHANGES IN THE VALUES OF OTHER CELLS.


# This 'Event' class is essentially a list of functions that need to be invoked when a particular event
# happens in the system, to make modifications in the system or to notify components of the system
# This 'Event' class is an Observer. It calls every function assigned to its list with all the arguments passed
# to it.
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self: # Call all the functions (subscribers) of this particular Event Observer
            item(*args, **kwargs)

# The Event Observer
class PropertyObservable:
    def __init__(self):
        # An 'Event' instance that people can subscribe to
        self.property_changed = Event()

class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__() # initialize the parent class 'PropertyObservable' as well
        self._age = age # private attribute not to be accessed outside this class
        
    @property
    def age(self):
        return self._age
        
    @age.setter
    def age(self, value):
        if self._age == value: # If there is no change in the value, return None
            return
        # If the 'age' value is different from current 'age', update it and add the updation event handler
        # to the list of event handlers in the 'Event' instance associated with this Observer
        self._age = value
        self.property_changed('age', value) # the arguments are for the list of functions to be called  


# A class to monitor the age of a person and notify if when their age changes about their driving permissions
class TrafficAuthority:
    def __init__(self, person):
        self.person = person
        person.property_changed.append(self.person_changed) # subscribe this instance to the 'property_changed'
        # Event Observer of a 'Person' instance called 'person' by adding the age modification event handler
        # of this instance called 'person_changed' to the 'property_changed' Event Observer's function call list

    def person_changed(self, name, value):
        # Note that 'name' and 'value' arguments will be passed to this function in 'self.property_changed'
        # by the __call__() method of the 'Event' instance! We use the 'name' argument to check if 'age' is the
        # property modified in the 'Person' instance and if so, we handle it by notification in the system.
        if name == 'age':
            if value < 16:
                print('Sorry, you still cannot drive')
            else:
                print('Okay, you can drive now')
                # once the person is of driving permitted age, we can unsubscribe the person from the age
                # property modification Event Observer.
                self.person.property_changed.remove(self.person_changed)


# if __name__ == '__main__':
#     p = Person()
#     ta = TrafficAuthority(p)
#     for age in range(14, 20):
#         print(f'Setting age to {age}')
#         p.age = age




# PROPERTY OBSERVER FOR A DEPENDENT PROPERTY


class Person(PropertyObservable):
    def __init__(self, age=0):
        super().__init__() # initialize the parent class 'PropertyObservable' as well
        self._age = age # private attribute not to be accessed outside this class
        
    @property
    def age(self):
        return self._age

    @property
    def can_vote(self):
        return self._age >= 18
        
    @age.setter
    def age(self, value):
        if self._age == value: # If there is no change in the value, return None
            return
            
        old_can_vote = self.can_vote # cache the older 'self.can_vote' value before potentially changing 'age'
        # to the passed value and re-computing 'self.can_vote'

        # If the 'age' value is different from current 'age', update it and add the updation event handler
        # to the list of event handlers in the 'Event' instance associated with this Observer
        self._age = value
        self.property_changed('age', value)

        if old_can_vote != self.can_vote: # If the cached old 'self.can_vote' property and the re-computed
            # 'self.can_Vote' properties are different, ie, the age was updated
            self.property_changed('can_vote', self.can_vote)
        
        # You can have properties that depend on other properties of the instance and such cases can pose
        # a problem. How do we send notifications on changes to the voting ability of this person ?
        
        
if __name__ == '__main__':
    def person_changed(name, value):
        if name == 'can_vote': # If the voting status has changed, then notify. We use the 'name' argument
            # passed to this function in the 'Event' instance to check if the value modified is the 'can_vote'
            # property of the 'Person' instance
            print(f'Voting ability changed to {value}')

    p = Person()
    p.property_changed.append(person_changed)
    for age in range(16, 20):
        print(f'Changing age to {age}')
        p.age = age





# EXERCISE 


# Imagine a game where one or more rats can attack a player. Each individual rat has an initial attack value 
# of 1. However, rats attack as a swarm, so each rat's attack value is actually equal to the total number 
# of rats in play.
# Given that a rat enters play through the initializer and leaves play (dies) via its __exit__ method, please 
# implement the 'Game' and 'Rat' classes so that, at any point in the game, the 'attack' value of a rat is 
# always consistent.


# MY IMPLEMENTATION

class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

class Game:
    def __init__(self):
        self.rats = []
        self.swarm = Event()
        
def attack_buff(game, value):
    for rat in game.rats:
        rat.attack = value

class Rat:
    def __init__(self, game):
        self.game = game
        self.attack = 1
        self.game.rats.append(self)
        self.game.swarm.append(attack_buff)
        self.game.swarm(self.game, len(self.game.rats))
    
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.rats.remove(self)
        self.game.swarm.append(attack_buff)
        self.game.swarm(self.game, len(self.game.rats))
        
    def attack_buff(self, sender, value):
        sender.attack = value


game = Game()
rat = Rat(game)
print(rat.attack)
rat2 = Rat(game)
print(rat.attack)
print(rat2.attack)
with Rat(game) as rat3:
    print(rat.attack)
    print(rat2.attack)
    print(rat3.attack)
print(rat.attack)
print(rat2.attack)



# ALTERNATE IMPLEMENTATION

class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

class Game:
    def __init__(self):
        # have three seperate events for a rat entering the game, a rat dying and notificationsabout rats
        self.rat_enters = Event()
        self.rat_dies = Event()
        self.notify_rat = Event()


class Rat:
    def __init__(self, game):
        self.game = game
        self.attack = 1

        game.rat_enters.append(self.rat_enters)
        game.notify_rat.append(self.notify_rat)
        game.rat_dies.append(self.rat_dies)

        self.game.rat_enters(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.rat_dies(self)

    def rat_enters(self, which_rat):
        if which_rat != self:
            self.attack += 1
            self.game.notify_rat(which_rat)

    def notify_rat(self, which_rat):
        if which_rat == self:
            self.attack += 1

    def rat_dies(self, which_rat):
        self.attack -= 1
