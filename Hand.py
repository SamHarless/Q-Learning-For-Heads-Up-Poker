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
    
    def showBoard(self):
        printArr = []
        for card in self.board:
            printArr.append(str(card))
        return printArr
    
    def evaluateHands(self):
        hand1 = self.players[0].hand
        hand2 = self.players[1].hand
    
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
            print("The current board is: " + self.showBoard())

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

            if i == 0:
                burn = self.deck.drawTop()
                self.board[0] = self.deck.drawTop()
                self.board[1] = self.deck.drawTop()
                self.board[2] = self.deck.drawTop()
            elif i is not 3:
                burn = self.deck.drawTop()
                self.board[i+3] = self.deck.drawTop()
            i+=1

        # reward pot
        if fold == True:
            for player in self.players:
                if player.decision is not 'fold':
                    potValue = self.pot.getValue()
                    chipDict = self.player.chips.valueToChips(potValue)
                    self.player.chips.addChips(chipDict)
        

        

                    


