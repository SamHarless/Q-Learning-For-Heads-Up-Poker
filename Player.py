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

    def playInitial(self, pot):
        print("Your hand is " + str(self.hand))
        choice = input("Please enter a number:\n1.....Check\n2.....Bet\n3.....Fold")
        if int(choice) == 1:
            self.descision = 'check'
        elif int(choice) == 2:
            print("Your current total is " + str(self.chips.chips))
            print("Enter ! to quit at anytime")
            betsDict = {}
            while bet_amount != '!' or bet_value != '!':
                bet_value = int(input('What denomination would you like to bet: '))
                bet_amount = int(input('How much of that denomination do you want to bet: '))

                betsDict[bet_value] = bet_amount
            self.chips.betChips(betsDict, pot)
            self.descision = 'bet'
        else:
            self.descision = 'fold'

