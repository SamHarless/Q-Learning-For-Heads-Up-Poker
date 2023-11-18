def Chips():
    def __init__(self):
        # give same starting chips to every player
        # key is monetary value : value is amount of chips
        self.lowestDenom = '5'

        self.chips = {
            self.lowestDenom : 40,
            '25' : 40,
            '100' : 40,
            '500' : 20,
            '1000' : 10
        }
    
    def betChips(self, amountBetDict):
        # if player bets 5$, amountBetDict = {'5' : 1}
        for (chipValue, chipAmount) in amountBetDict:
            if self.chips[chipValue] - chipAmount >= 0:
                self.chips[chipValue] = self.chips[chipValue] - chipAmount
    
    def getTotal(self):
        return sum([int(amount) * val for amount, val in self.chips])
    
    def bigBlind(self, pot):
        self.chips[self.lowestDenom] = self.chips[self.lowestDenom] - 1
        pot.add(int(self.lowestDenom))