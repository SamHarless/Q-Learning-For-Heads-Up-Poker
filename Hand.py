import Deck
import Card
import Pot

def Hand():
    def __init__(self, players, deck, bigBlind):
        self.players = players
        self.deck = deck
        self.bigBlind = bigBlind
        self.pot = Pot()
        self.board = [Card(-1,-1), Card(-1,-1), Card(-1,-1), Card(-1,-1), Card(-1,-1)]

    def startHand(self):
        # get big blind from player
        self.players[self.bigBlind].chips.bigBlind(self.pot)

        # deal cards
        self.players[self.bigBlind].assignHand()
        self.players[not self.bigBlind].assignHand()

        
        