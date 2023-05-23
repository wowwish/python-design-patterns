# The Mediator Design Pattern facilitates communication between Components (classes)
# Components (classes) can go in and out of a system at any time. For example: 
#   * Chat room participants can join a room, leave a room, can go to a different room etc.
#   * Players in an MMORPG  can leave a game, suffer disconnection to game server
# It makes no sense to have direct reference to one another among these Components in such cases as such
# direct references may go dead anytime (when one of the Components is removed for example).
# Here, the Mediator pattern can be used to make every single Component that needs to have communication, 
# to refer to a central Component (The Mediator) that facilitates the communication!

# A Mediator is a Component (class) that facilitates communication between other Components without them 
# neccessarily being aware of each other or having direct access (reference) to each other. 
# A Mediator is referenced by each object in the system using an internal attribute. The Mediator also 
# engages in bi-directional communication with its connected components (The Mediator has methods that
# the Components referencing it can call and the Components referencing the Mediator have their own methods
# that the Mediator can call!). 
# Event Processing (eg. Reactive extensions) libraries make communication between Components easier 
# to implement via the Mediator.



# A Classic implementation of the Mediator Design Pattern is a Chatroom. People can join or leave the Chatroom
# but they don't neccessarily be aware of one another unless they are sending a direct message. General meesage
# in the Chatroom can be viewed by everyone in the Chatroom and people donot need to be aware of one another
# to see these general messages.


class Person:
    def __init__(self, name):
        self.name = name
        self.chat_log = [] # a list of messages sent/recieved by this person
        self.room = None # The 'ChatRoom' instance to which this person belongs

    # a method to recieve a message from a sender and store it in the log of a 'Person' instance
    def recieve(self, sender, message):
        s = f'{sender}: {message}'
        print(f'[{self.name}\'s chat session] {s}')
        self.chat_log.append(s)

    # a method to allow a person to send a general message in the chat room (to all other people in the chat
    # room except self)
    def say(self, text):
        self.room.broadcast(self.name, text)

    # a method to allow the person to send a private message to another person
    def private_message(self, who, text):
        self.room.message(self.name, who, text)


# The Central Mediator that allows communication between 'Person' instances
class ChatRoom:
    def __init__(self):
        self.people = [] # list to store all people who are part of this 'ChatRoom' instance

    # method to add a person to this 'ChatRoom' instance
    def join(self, person):
        join_msg = f'{person.name} joins the chat'
        self.broadcast('room', join_msg) # send a message to all people in the current 'ChatRoom' instance
        person.room = self # set the chatroom of a person to the current instance
        self.people.append(person) # add the person to this ChatRoom instance
    
    def broadcast(self, source, message):
        # send the message to every 'Person' instance in 'self.people' except for the source 'Person' instance
        for p in self.people:
            if p.name != source:
                p.recieve(source, message)

    # a method to send a direct or private message from a sender to another person in the chat room
    def message(self, source, destination, text):
        for p in self.people:
            if p.name == destination:
                p.recieve(source, text)


# if __name__ == '__main__':
#     room = ChatRoom()
#     john = Person('John')
#     jane = Person('Jane')
#     room.join(john) # no one in the room to get the message of John joining the chat room
#     room.join(jane) # John recieves a general message that Jane has joined the chat room
#     john.say('hi room!') # Jane recieves this general message to the chat room from John
#     jane.say('oh, hey John') # John recieves this general message to the chat room from Jane
#     simon = Person('Simon') 
#     room.join(simon) # Both John and Jane get the message of Simon joining the chat room
#     simon.say('hi everyone!') # Both John and Jane get this general message from Simon
#     jane.private_message('Simon', 'glad you could join us!') # Only Simon recieves this private message from Jane


# THE PREVIOUS IMPLEMENTATION OF MEDIATOR CASES CIRCULAR DEPENDENCY BETWEEN THE 'ChatRoom' AND 'Person' 
# INSTANCES WHICH IS A VIOLATION OF DEPENDENCY INVERSION PRINCIPLE!

# AN ALTERNATE APPROACH IS TO USE AN EVENT BASED MEDIATED USING PRINCIPLES FROM THE OBSERVER PATTERN:

# An Event (subscriber list) implemented from the Observer Pattern
class Event(list):
    # the __call__() method when implemented makes every object of this class as a callable object that performs 
    # the underlying logic associated with __call__(). In the Observer Pattern, we use it to call a list of 
    # functions, one by one in order, using the same arguments that were supplied when the object itself was 
    # called like a function. The objects of this class can therefore be called like a function and can
    # also be used like normal class instances.
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


# The Mediator Component for modelling a Soccer Game. The Game generates Events which Players, Coaches and
# Viewers can subscribe to and get information about something happening in the Game. 
class Game: # A centrally available Mediator component that is injected into 'Player' and 'Coach' classes
    def __init__(self):
        self.events = Event() # any player/coach/viewer instance can take Game.events and subscribe to it

    # utility method for firing (invoking) 'self.events' (list of functions to pass on information)
    def fire(self, args):
        self.events(args)

# a handler that collects information on who scored a goal and how many goals have been scored by that player 
# in the Game
class GoalScoredInfo:
    def __init__(self, who_scored, goals_scored):
        self.who_scored = who_scored
        self.goals_scored = goals_scored


class Player:
    def __init__(self, name, game): # Connect the 'Player' instance to the Mediator 'Game' class
        self.name = name
        self.game = game
        self.goals_scored = 0 # total goals scored by this player in this game

    # A method to handle messaging when a goal is scored by this player
    def score(self):
        self.goals_scored += 1
        args = GoalScoredInfo(self.name, self.goals_scored) # Use handler classes to pass on information
        # between Components that are connected through the Mediator 'Game' class (Coach and Player in this case)
        self.game.fire(args)

class Coach:
    def __init__(self, game): # connect the 'Coach' instance also to the Mediator 'Game' class
        game.events.append(self.celebrate_goal)

    def celebrate_goal(self, args): # 'args' relates to a 'GoalScoredInfo' instance here
        # Coach congratulates a player only for the first two goals that the player scores
        if isinstance(args, GoalScoredInfo) and args.goals_scored < 3:
            print(f'Coach says: well done, {args.who_scored}')


if __name__ == '__main__':
    game = Game()
    player = Player('Sam', game)
    coach = Coach(game)

    player.score()
    player.score()
    player.score()





# EXERCISE


# Our system has any number of instances of 'Participant' instances. Each Participant has a 'value' integer 
# attribute, initially zero.
# A participant can 'say()' a particular value, which is broadcast to all other participants. 
# At this point in time, every other participant is obliged to increase their value by the value being broadcast.
# Example:
#   * Two participants start with values 0 and 0 respectively
#   * Participant 1 broadcasts the value 3. We now have Participant 1 value = 0, Participant 2 value = 3
#   * Participant 2 broadcasts the value 2. We now have Participant 1 value = 2, Participant 2 value = 3


# An Event (subscriber list) implemented from the Observer Pattern
class Event(list):
    # the __call__() method when implemented makes every object of this class as a callable object that performs 
    # the underlying logic associated with __call__(). In the Observer Pattern, we use it to call a list of 
    # functions, one by one in order, using the same arguments that were supplied when the object itself was 
    # called like a function. The objects of this class can therefore be called like a function and can
    # also be used like normal class instances.
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

# The Mediator class
class Mediator:
    def __init__(self):
        self.alerts = Event()
    
    # call all the functions in the 'Event' list referenced in 'self.alerts'
    def broadcast(self, sender, value):
        self.alerts(sender, value)

# From the perspective of the Observer Pattern, this Participant class becomes the Subject and the Observer
class Participant:
    def __init__(self, mediator):
        self.value = 0
        self.mediator = mediator # every participant is associated with a mediator system
        self.mediator.alerts.append(self.mediator_alert) # whenever a new participant is created, the 
        # participant's 'mediator_alert' method is added to the 'Event' subscriber list

    def say(self, value):
        self.mediator.broadcast(self, value) # 'self' and 'value' are passed on as '*args' and '**kwargs'
        # for the __call__() method of the 'Event' instance in the Mediator instance associated with 'self'
    
    # The action method which increments the value of all other participants in the system (linked to 
    # the same Mediator)
    def mediator_alert(self, sender, value):
        if sender != self:
            self.value += value