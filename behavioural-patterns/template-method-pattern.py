# The Template Method Design Pattern specifies a high-level blueprint for an algorithm to be completed
# by inheritors.
# Algorithms can be decomposed into common parts as well as specifics (similar to the Strategy Pattern)
# The Strategy Pattern does this through "Decomposition", ie, a High-level algorithm expects strategies
# to conform to an Interface that provides the High-level algorithmic blueprint. Then, concrete 
# implementations of this Interface is done in the Strategy Pattern. 
# The Template Method Design Pattern does the same thing, but through Inheritance! The overall algorithm
# is defined in a base class that makes use of several abstract members. Inheritors of this base class
# override the abstract members and the template method from the base class is invoked to get the work
# done.

# The Template Method is a construct that allows us to define the 'skeleton' of the algorithm in base 
# class (parent class), where the constituent parts are defined as abstract methods / properties.
# The concrete implementations ate defined in sub-classes that inherit this base (algorithm) class and
# provide the neccessary overrides of its methods


from abc import ABC # For creating abstract base class


# A high-level bluewprint for a board game - A Template
class Game(ABC):
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.current_player = 0

    # The Template Method - implements how the board game progresses
    def run(self):
        self.start()
        while not self.have_winner:
            self.take_turn()
        print(f'Player {self.winning_player} wins!')
    
    def start(self): pass

    @property
    def have_winner(self): pass

    def take_turn(self): pass

    @property
    def winning_player(self): pass


# A chess game simulation that inherits the high-level 'Game' Template and implements the specifics
class Chess(Game):
    def __init__(self):
        super().__init__(2)
        self.max_turns = 10
        self.turn = 1

    def run(self):
        super().run()

    def start(self):
        print(f'Starting a game of chess with {self.number_of_players} players')
    
    @property
    def have_winner(self):
        return self.turn == self.max_turns

    def take_turn(self):
        print(f'Turn {self.turn} taken by Player {self.current_player}')
        self.turn += 1
        self.current_player = 1 - self.current_player # cycle between 0 and 1
    
    @property
    def winning_player(self):
        return self.current_player
    

if __name__ == '__main__':
    chess = Chess()
    chess.run()





# EXERCISE


# Imagine a typical collectible card game which has cards representing creatures. 
# Each creature has two values: Attack and Health. Creatures can fight each other, dealing their 
# Attack damage, thereby reducing their opponent's health.
# The class 'CardGame' implements the logic for two creatures fighting one another. However, the exact 
# mechanics of how damage is dealt is different:
#   * TemporaryCardDamage : In some games (e.g., Magic: the Gathering), unless the creature has been 
#     killed, its health returns to the original value at the end of combat.
#   * PermanentCardDamage : In other games (e.g., Hearthstone), health damage persists.
# You are asked to implement classes 'TemporaryCardDamageGame' and 'PermanentCardDamageGame' that 
# would allow us to simulate combat between creatures.

# Some examples:
#   * With temporary damage, creatures 1/2 and 1/3 can never kill one another. With permanent damage, 
#     second creature will win after 2 rounds of combat.
#   * With either temporary or permanent damage, two 2/2 creatures kill one another.


from abc import ABC

class Creature:
    def __init__(self, attack, health):
        self.health = health
        self.attack = attack

class CardGame(ABC):
    def __init__(self, creatures):
        self.creatures = creatures

    # return -1 if both creatures alive or if both dead after combat
    def combat(self, c1_index, c2_index):
        c1 = self.creatures[c1_index]
        c2 = self.creatures[c2_index]
        self.hit(c1, c2)
        self.hit(c2, c1)
        if c1.health > 0 and c2.health > 0:
            return -1
        elif c1.health > 0 and c2.health <= 0:
            return c1_index
        elif c2.health > 0 and c1.health <= 0:
            return c2_index
        else:
            return -1
    
    def hit(self, attacker, defender):
        pass  # implement this in derived classes


class TemporaryDamageCardGame(CardGame):
    def hit(self, attacker, defender):
        if attacker.attack >= defender.health:
            defender.health -= attacker.attack


class PermanentDamageCardGame(CardGame):
    def hit(self, attacker, defender):
        defender.health -= attacker.attack