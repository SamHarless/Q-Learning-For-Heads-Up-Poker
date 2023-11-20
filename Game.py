import Deck
import Player
import Hand
import random

class Game:
    def __init__(self):
        self.players = [Player.Player(0), Player.Player(1)]
        self.bigBlind = 0 if random.randint(0,1) == 0 else 1

    def run(self):
        while self.players[0].chips.getTotal() > 0 and self.players[1].chips.getTotal() > 0:
            self.deck = Deck.Deck()
            currentHand = Hand.Hand(self.players, self.deck, self.bigBlind)
            currentHand.startHand()
            self.bigBlind = int(not self.bigBlind)

hi = Game()
hi.run()
