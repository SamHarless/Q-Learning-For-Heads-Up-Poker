import random

class Card(object):

    def __init__(self,suitIn, val):
        # PLACEHOLDER CARD FOR BOARD
        if val < 0 or suitIn < 0:
            self.suit = -1
            self.value = -1

        # Normal card assignment
        self.suit = suitIn
        self.value = val

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.name()
    
    def name(self):
        if self.value == 1:
            val = "Ace"
        elif self.value == 11:
            val = "Jack"
        elif self.value == 12:
            val = "Queen"
        elif self.value == 13:
            val = "King"
        else:
            val = self.value
        if self.suit == 0:
            s = "Hearts"
        elif self.suit == 1:
            s = "Diamonds"
        elif self.suit == 2:
            s = "Spades"
        else:
            s = "Clubs"

        return (str(val)+" of "+str(s))