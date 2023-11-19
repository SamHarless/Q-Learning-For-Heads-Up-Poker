def Chips():
    def __init__(self):
        # give same starting chips to every player
        # key is monetary value : value is amount of chips

        self.denoms = ['5', '25', '100', '500', '1000']

        self.chips = {
            self.denoms[0] : 40,
            self.denoms[1] : 40,
            self.denoms[2] : 40,
            self.denoms[3] : 20,
            self.denoms[4] : 10
        }
    
    def betChips(self, amountBetDict, pot):
        # if player bets 5$, amountBetDict = {'5' : 1}
        for (chipValue, chipAmount) in amountBetDict:
            if self.chips[chipValue] - chipAmount >= 0:
                self.chips[chipValue] = self.chips[chipValue] - chipAmount
                pot.add(getTotal(amountBetDict))
            else:
                print("You do not have enough chips to bet!")
    
    def getTotal(self):
        return sum([int(amount) * val for amount, val in self.chips])
    
    def bigBlind(self, pot):
        self.chips[self.lowestDenom] = self.chips[self.lowestDenom] - 1
        pot.add(int(self.lowestDenom))
    
    def addChips(self, amountDict):
        for (chipValue, chipAmount) in amountDict:
            self.chips[chipValue] = self.chips[chipValue] + chipAmount

    def valueToChips(self, potValue):
        chipDict = {}
        for denom in reversed(self.denoms):
            amount = potValue // int(denom)
            potValue = potValue - (int(denom) * amount)
            chipDict[denom] = amount
        return chipDict
            