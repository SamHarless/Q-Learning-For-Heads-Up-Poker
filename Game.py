import Deck
import Player
import Hand
import random

def Game():
    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.bigBlind = 0 if random.randint(0,1) == 0 else 1
        while self.players[0].getTotal() > 0 and self.players[1].getTotal() > 0:
            self.deck = Deck()
            currentHand = Hand(self.players, self.deck, self.bigBlind)
