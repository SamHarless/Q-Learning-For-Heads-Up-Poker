import random

class Card(object):

    def __init__(self,suitIn, val):

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

        return (str(val)+" of "+str(self.suit))