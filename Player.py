from Card import Card
import random
import Chips

class Player(object):
    def __init__(self, id):
        self.id = id
        self.chips = Chips()
        self.hand = []
    
    def assignHand(self, deck):
        self.hand = [deck.drawTop(), deck.drawTop()]