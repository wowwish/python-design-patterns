# The Chain-Of-Responsibility Pattern corresponds to a seuqnce of handlers processing an event one after another
# The Chain-of-Responsibility Pattern is all about chaining several components (classes) who all get a
# chance to process a command or a query, optionally having default processing implementation and an
# ability to terminate the processing chain.

# The Chain of Responsibility can be implemented either as a linked-list of references (to methods) or you
# can have a centralized construct which simply keeps a list of objects that "paints" other objects (you
# enlist modifier objects in the chain, typically controlling their order of execution and then fire off the 
# chain. Every object in the chain can pass the ball along to the next chain or terminate the chain. 
# You can also implement the magic function '__exit__()' in every modifier object to remove the modifier 
# object from the chain once it is used/applied)

# Take the situation of unethical behaviour by an employee of a company. Who takes the blame in this situation ?
#   * Employee ?
#   * Manager ?
#   * CEO ?
# It depends on how grievous the error is and how institutional the unethical behaviour is

# As another example, think of clicking on a graphical element (like a button) in a form.
#   * The button can handle the event and stop further processing
#   * Maybe the button belongs to a groupbox and the event is bubbled up to the groupbox for handling
#   * Maybe the underlying window handles the click

# As another example, consider a collectible card game where Creatures have attack and defense values that
# can be affected by other cards in your deck.


# Consider a multiplayer game with creatures where you want to make the creatures pick a power-up and
# have its stats modified
class Creature:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def __str__(self):
        return f'{self.name} ({self.attack}/{self.defense})'


class CreatureModifier:
    def __init__(self, creature):
        self.creature = creature
        # next modifier in the chain of stat modifiers picked up by the creature (you can modify a creature
        # more than once! the 'self.next_modifier' is a reference to a creature stat modifier function
        # that we are going to call after the current stat modifier function is applied on the creature)
        self.next_modifier = None

    # method to add another modifier to the modifier chain and grow the chain of responsibility
    def add_modifier(self, modifier):
        if self.next_modifier:  # If there is already a modifier yet to be applied on the creature
            # add the new modifier to the next modifier's
            self.next_modifier.add_modifier(modifier)
            # next modifier (chaining)
        else:
            # otherwise, set the new modifier as the immediate next modifier
            self.next_modifier = modifier
            # for the creature

    # This method applies the current modifier to the creature
    def handle(self):
        if self.next_modifier:
            self.next_modifier.handle()


class DoubleAttackModifier(CreatureModifier):
    def handle(self):
        print(f'Doubling {self.creature.name}\'s attack')
        self.creature.attack *= 2
        # invoke the base class handler() method to propagate the chain of responsibility
        super().handle()
        # and call the handle() method of the next modifier in the 'Creature' instance's modifier chain


class IncreaseDefenseModifier(CreatureModifier):
    def handle(self):
        # Only increase the defense if the attack value is >= 2
        if self.creature.attack <= 2:
            print(f'Increasing {self.creature.name}\'s defense')
            self.creature.defense += 1
        # invoke the base class handler() method to propagate the chain of responsibility
        super().handle()
        # and call the handle() method of the next modifier in the 'Creature' instance's modifier chain

# A modifier that stops or breaks the chain propagation


class NoBonusesModifier(CreatureModifier):
    # We terminate the chain here, by not calling the base class's handle() method which will apply the next
    # modifier in the chain.
    def handle(self):
        print('No bonuses for you')


if __name__ == '__main__':
    goblin = Creature('Goblin', 1, 1)
    print(goblin)
    # chain of responsibility implementation
    root = CreatureModifier(goblin)
    # root.add_modifier(NoBonusesModifier(goblin))
    root.add_modifier(DoubleAttackModifier(goblin))
    root.add_modifier(IncreaseDefenseModifier(goblin))
    root.add_modifier(DoubleAttackModifier(goblin))
    root.handle()  # This applies all the modifiers in the chain one by one
    print(goblin)

    print()
    print()
    print()


# COMMAND AND QUERY SEPERATION
# A Command asks for an action or change (eg. please set the attack value of creature to 2)
# A query asks for information (eg. give the current attack value of the creature)
# The Command-Query-Seperation (CQS) means having seperate means of sending Commands and Queries
# Example: directly access fields with in a database with a Query (Please give me the contents of a field)
# # or with a Command (Please set the field to these set of values)
# The Chain of Responsibility Pattern allows the usage of Listeners that override and modify the behaviour
# of Commands and Queries.


# WE CAN ALSO APPLY MODIFIERS WITHOUT CALLING THE BASE CLASS HANDLER USING AN EVENT BROKER
# (THE EVENT BROKER IS SIMILAR TO OBSERVER DESIGN PATTERN)
# WE ALSO NEED COMMAND QUERY SEPERATION IMPLEMENTED IN THIS APPROACH



# An Event is essentially a list of functions that you can call one by one
class Event(list):
    # The __call__() method is used to define the logic when an instance of this 'Event' class is called
    # with some arguments passed to it
    def __call__(self, *args, **kwargs):
        # here, we call all the query functions that this 'Event' instance contains
        for item in self:
            item(*args, **kwargs)

from enum import Enum  # To create Enumerators

# An enumerator for the attributes you want to query from creature
class WhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2


# The query class to hold query result of a particular stat of a 'Creature' instance. 
# Stat Modifiers are applied on this query result ('Query' instance's 'value' attribute).
class Query:
    def __init__(self, creature_name, what_to_query, default_value):
        self.value = default_value
        self.creature_name = creature_name
        self.what_to_query = what_to_query # can be any of the stat from the Enum 'WhatToQuery'


# The Event Broker class (An Observer)
class Game:
    def __init__(self):
        # Remember that 'Event' is a list of command/query functions that you can call
        self.modifiers = Event()

    # method to invoke all the 'handle()' stat modifier methods on corresponding creatures in the
    # game using the 'sender.name' information. The modifiers are applied only on the 'query.value' result
    # and not on the original stats of the creature instance itself!
    def perform_query(self, sender, query):
        # here, the 'Event' instance is called and the Event.__call__() method is invoked with two
        # arguments - the 'sender' and the 'query' for every modifier function in the 'Event' list instance
        self.modifiers(sender, query)


class Creature:
    # 'game' is the central even broker that will take care of the chain of responsibility,
    # because every creature is part of a game
    def __init__(self, game, name, attack, defense):
        self.initial_defense = defense
        self.initial_attack = attack
        self.name = name
        self.game = game

    # The 'attack' and 'defense' properties are dynamically obtained everytime. The 'self.game.perform_query()'
    # performs all the 
    @property
    def attack(self):
        # build query result using the event broker 'game'
        q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
        # Here, the 'sender' argument to the Event.perform_query() method is 'self'. All the modifiers
        # in 'self.game.modifiers' are then applied to this query object by the corresponding 
        # 'handle(source, query)' calls 
        self.game.perform_query(self, q)
        # return the final stat afer all modifiers are applied 
        return q.value 

    @property
    def defense(self):
        # query using the event broker 'game'
        q = Query(self.name, WhatToQuery.DEFENSE, self.initial_defense)
        # Here, the 'sender' argument to the Event.perform_query() method is 'self'. All the modifiers
        # in 'self.game.modifiers' are then applied to this query object by the corresponding 
        # 'handle(source, query)' calls 
        self.game.perform_query(self, q)
        # return the final stat afer all modifiers are applied 
        return q.value

    def __str__(self):
        return f'{self.name} ({self.attack}/{self.defense})'


from abc import ABC # For creating abstract base classes (classes with only method definition and no method body)

# An abstract base-class for creature modifiers to inherit and implement
class EBCreatureModifier(ABC):
    def __init__(self, game, creature):
        self.game = game
        self.creature = creature
        # add the handle() method (which modifies a particular stat of creature) from 'self' to the 'Event' 
        # list created in the Event Broker class 'Game'. Each 'handle()' function modifies the stats of 
        # a creature in a particular way / under particular conditions.
        self.game.modifiers.append(self.handle)
    
    # This method applies the specific stat changes to a creature. It has to be implemented properly
    # in every modifier class that inherits this 'EBCreatureModifier' class
    def handle(self, sender, query):
        pass
    
    # You can also make these creature stat modifier have a lifetime (the modifier is applied only
    # within the scope of a 'with' keyword for example, similar to open() or a database connection
    # that automatically closes outside the scope of a 'with' keyword).
    # The __enter__() and __exit__() methods (context manager methodss) allow you to implement objects which can 
    # be used easily with the 'with' statement. A class that implements both of these two magic methods becomes
    # a Context Manager class
    def __enter__(self): # in-built method called at the start of the 'with' keyword block
        # The 'with' statement will bind this method’s return value to the target(s) specified 
        # in the 'as' clause of the statement, if any.
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # The parameters describe the exception that caused the context to be exited. 
        # If the context was exited without an exception, all three arguments will be None.
        # If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it 
        # from being propagated), it should return a true value. Otherwise, the exception will be 
        # processed normally upon exit from this method.
        # unsubscribe the object from the modifier when exiting the scope of the 'with' keyword block
        self.game.modifiers.remove(self.handle)


# Event-Broker based Creature instance Modifier
class EBDoubleAttackModifier(EBCreatureModifier):
    # The constructor for this class is inherited from the base class 'EBCreatureModifier'
    # override the 'handle()' method of 'EBCreatureModifier'
    def handle(self, sender, query):
        # If the name of attribute of 'sender' (which is the Creature) is the same as the creature name
        # of the 'Creature' instance to which this modifier is to be applied and the queried attribute is 
        # the attack stat of the creature
        if sender.name == self.creature.name and query.what_to_query == WhatToQuery.ATTACK:
            # The query value is modified here. Remember that the query result is returned only after applying
            # all the modifiers in the 'self.modifiers' (Event() instance) of the Event Broker 'game'
            # This handle() function is added to the list of modifiers ('self.modifiers') 
            query.value *= 2 

# Event-Broker based Creature instance Modifier
class EBIncreaseDefenseModifier(EBCreatureModifier):
    # The constructor for this class is inherited from the base class 'EBCreatureModifier'
    # overload the 'handle()' method of 'EBCreatureModifier'
    def handle(self, sender, query):
        # If the name of attribute of 'sender' (which is the Creature) is the same as creature name of the
        # 'Creature' instance to which this modifier is to be applied and the queried attribute is the 
        # defense stat of the creature
        if (sender.name == self.creature.name and query.what_to_query == WhatToQuery.DEFENSE):
            query.value += 3

if __name__ == '__main__':
    game = Game() # Instantiate the Event Broker class
    goblin = Creature(game, 'Strong Goblin', 2, 2) # Instantiate a creature
    print(goblin)
    with EBDoubleAttackModifier(game, goblin): # This modifier is applied to 'goblin' as long as it is inside this scope
        print(goblin)
        with EBIncreaseDefenseModifier(game, goblin):
            print(goblin) # The increased defense modifier is applied to 'goblin' as long as it is inside this scope
    print(goblin) # print the 'Creature' instance again outside the scope of the with block where the
    # 'EBDoubleAttackModifier' is applied to the 'Creature' instance






# EXERCISE 

# You are given a game scenario with classes Goblin and GoblinKing. Please implement the following rules:
#   * A goblin has base 1 attack/1 defense (1/1), a goblin king is 3/3.
#   * When the Goblin King is in play, every other goblin gets +1 Attack.
#   * Goblins get +1 to Defense for every other Goblin in play (a GoblinKing is a Goblin!).

# Example:
#   * Suppose you have 3 ordinary goblins in play. Each one is a 1/3 (1/1 + 0/2 defense bonus).
#   * A goblin king comes into play. Now every goblin is a 2/4 (1/1 + 0/3 defense bonus from each 
#     other + 1/0 from goblin king)

# The state of all the goblins has to be consistent as goblins are added and removed from the game.
# Note: creature removal (unsubscription) does not need to be implemented.


from abc import ABC # for creating abstract base classes
from enum import Enum # for enumerator creation

# creature removal (unsubscription) ignored in this exercise solution

# Enumerator for Stats of a Creature
class ExcWhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2

# Class to build a query result
class ExcQuery:
    def __init__(self, initial_value, what_to_query):
        self.what_to_query = what_to_query
        self.value = initial_value

# Abstract Class (with abstract methods and an initializer) that will be inherited and overloaded by
# every Creature type class.
class ExcCreature:
    def __init__(self, game, attack, defense):
        self.game = game
        self.initial_attack = attack
        self.initial_defense = defense
    
    # The stats of the creature are implemented as "properties" as they have to be dynamically built
    # during runtime, taking into account the effect of the creature stat modifiers.
    @property
    def attack(self): pass

    @property
    def defense(self): pass

    # This method takes care of the logic of how other creatures affect the stats of this creature and how
    # this creature affects the stats of other creatures
    def query(self):
        pass

# A Creature type called Goblin
class ExcGoblin(ExcCreature):
    def __init__(self, game, attack=1, defense=1):
        super().__init__(game, attack, defense)
    
    @property
    def attack(self):
        q = ExcQuery(self.initial_attack, ExcWhatToQuery.ATTACK)
        for c in self.game.creatures:
            # apply the stat modifiers on the query result that was built. Since other 'ExcCreature' instances
            # can affect the stat of this instance, we loop through every every 'ExcCreature' instance in
            # 'self.game.creatures' (including this instance itself)
            c.query(self, q)
        # return the final stat afer all modifiers are applied
        return q.value
    
    @property
    def defense(self):
        q = ExcQuery(self.initial_defense, ExcWhatToQuery.DEFENSE)
        for c in self.game.creatures:
            # apply the stat modifiers on the query result that was built. Since other 'ExcCreature' instances
            # can affect the stat of this instance, we loop through every every 'ExcCreature' instance in
            # 'self.game.creatures' (including this instance itself)
            c.query(self, q)
        # return the final stat afer all modifiers are applied    
        return q.value
    
    def __str__(self):
        return f'Goblin({self.attack}/{self.defense})'
    
    def query(self, source, query):
        # +1 defense for every other goblin in game
        if self != source and query.what_to_query == ExcWhatToQuery.DEFENSE:
            query.value += 1

# The king of goblins
class ExcGoblinKing(ExcGoblin):
    def __init__(self, game):
        super().__init__(game, 3, 3)
        
    def query(self, source, query):
        # +1 attack to every other goblin in game due to the presence of goblin king
        if self != source and query.what_to_query == ExcWhatToQuery.ATTACK:
            query.value += 1
        else:
            # the goblin king is also affected by stat modifications of other goblins in the game
            super().query(source, query)
    
    def __str__(self):
        return f'GoblinKing({self.attack}/{self.defense})'

# The Eveny-Broker class (implementing the Observer Pattern)
class ExcGame:
    def __init__(self):
        self.creatures = []


print()
print()
game = ExcGame()
goblin1 = ExcGoblin(game)
goblin2 = ExcGoblin(game)
goblin3 = ExcGoblin(game)
goblink = ExcGoblinKing(game)
game.creatures.append(goblin1)
game.creatures.append(goblin2)
game.creatures.append(goblin3)
game.creatures.append(goblink)
print(goblin1)
print(goblin2)
print(goblin3)
print(goblink)