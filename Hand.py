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
            for player in self.players: player.resestDecision()
            currentPlayer = self.bigBlind # big blind plays first
            lastBet = {'0' : 0}

            while self.decisionsMade() == False:
                print("Current Player is " + str(currentPlayer))
                lastBet = self.players[currentPlayer].play(self.pot, lastBet)

                if self.players[currentPlayer].decision == 'fold':
                    fold = True
                    break
                elif self.players[currentPlayer].decision == 'bet' or self.players[currentPlayer].decision == 'raise':
                    self.players[not currentPlayer].decision = None
                    currentPlayer = not currentPlayer
            # board for the cards
            # win logic
            if fold == True: 
                break

        # reward pot
        potValue = self.pot.getValue()

                    


