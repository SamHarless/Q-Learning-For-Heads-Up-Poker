from Card import Card
import random
import Chips

class Player(object):
    def __init__(self, id):
        self.id = id
        self.chips = Chips()
        self.hand = []
        self.descision = None
    
    def assignHand(self, deck):
        self.hand = [deck.drawTop(), deck.drawTop()]

    def resetDecision(self):
        # used for back and forth betting
        self.decision = None

    def play(self, pot, lastBet):
        print("Your hand is " + str(self.hand))
        numLastBet = sum([int(amount) * val for amount, val in lastBet])

        if numLastBet == 0:
            choice = input("Please enter a number:\n1.....Check\n2.....Bet\n3.....Fold")
            if int(choice) == 1:
                self.descision = 'check'
            elif int(choice) == 2:
                print("Your current total is " + str(self.chips.chips))
                print("Enter ! to quit at anytime")
                betsDict = {}
                while bet_amount != '!' or bet_value != '!':
                    bet_value = str(int(input('What denomination would you like to bet: ')))
                    bet_amount = int(input('How much of that denomination do you want to bet: '))

                    betsDict[bet_value] = bet_amount
                self.chips.betChips(betsDict, pot)
                self.descision = 'bet'
                return betsDict
            else:
                self.descision = 'fold'
        else:
            print("The last bet was: " + str(numLastBet))
            choice = input("Please enter a number:\n1.....Check\n2.....Call\n3.....Raise\n4.....Fold")
            if int(choice) == 1:
                self.descision = 'check'
            elif int(choice) == 2:
                self.chips.betChips(lastBet, pot)
                self.descision = 'call'
            elif int(choice) == 3:
                print("Your current total is " + str(self.chips.chips))
                print("Enter ! to quit at anytime")

                control = False
                while control == False:
                    betsDict = {}
                    while bet_amount is not '!' or bet_value is not '!':
                        bet_value = str(int(input('What denomination would you like to bet: ')))
                        bet_amount = int(input('How much of that denomination do you want to bet: '))

                        betsDict[bet_value] = bet_amount

                    if sum([int(amount) * val for amount, val in betsDict]) <= numLastBet:
                        print("You can not raise less than the previous bet.")
                    else:
                        control = True

                self.chips.betChips(betsDict, pot)
                self.descision = 'raise'
                return betsDict
            else:
                self.descision = 'fold'
        return {'0' : 0}
        

