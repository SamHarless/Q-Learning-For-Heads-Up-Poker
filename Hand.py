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

    def decisionsMade(self):
            for player in self.players:
                if player.decision == None:
                    return False
            return True
    
    def startHand(self):
        # get big blind from player
        self.players[self.bigBlind].chips.bigBlind(self.pot)

        # deal cards
        self.players[self.bigBlind].assignHand()
        self.players[not self.bigBlind].assignHand()

        fold = False
        i = 0
        while i < 4 and fold == False:
            for player in self.players: player.decision = None

            while self.decisionsMade == False:
                # big blind plays first
                self.players[self.bigBlind].playInitial()
                if self.players[self.bigBlind].decision == 'fold':
                    fold = True
                    break
