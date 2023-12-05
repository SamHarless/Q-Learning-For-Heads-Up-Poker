import numpy as np
from Card import Card
import random
import pygad
import Chips
import random
import Deck

class Player(object):
    def __init__(self, id):
        self.id = id
        self.chips = Chips.Chips()
        self.hand = []
        self.prevBet = 0
        self.decision = None
        self.game_over = False
    
    def assignHand(self, deck):
        self.hand = [deck.drawTop(), deck.drawTop()]

    def resetDecision(self):
        # used for back and forth betting
        self.decision = None

    def play(self, pot, lastBet, currBoard):
        print("Your hand is " + str(self.hand))
        numLastBet = sum([int(amount) * val for amount, val in lastBet.items()])
        choice = 3

        if numLastBet == 0:
            while int(choice) == 3:
                choice = input("Please enter a number:\n1.....Check\n2.....Bet\n3.....See your chip count\n4.....Fold\n")
                if int(choice) == 1:
                    self.decision = 'check'
                elif int(choice) == 2:
                    print("Your current total is " + str(self.chips.chips))
                    print("Enter ! as denomination to quit at anytime")
                    betsDict = {}
                    bet_value = ''
                    while True:
                        bet_value = str(input('What denomination would you like to bet: '))
                        if bet_value == '!':
                            break
                        bet_amount = int(input('How much of that denomination do you want to bet: '))

                        betsDict[bet_value] = bet_amount
                    self.chips.betChips(betsDict, pot)
                    self.decision = 'bet'
                    return betsDict
                elif int(choice) == 3:
                    print()
                    print(self.chips)
                else:
                    self.decision = 'fold'
        else:
            while int(choice) == 3:
                print("The last bet was: " + str(numLastBet))
                choice = input("Please enter a number:\n1.....Call\n2.....Raise\n3.....See your chip count\n4.....Fold\n")
                if int(choice) == 1:
                    if self.prevBet != 0:
                        prevSum = sum([int(amount) * val for amount, val in self.prevBet.items()]) # previous amount raised by you
                        lastSum = sum([int(amount) * val for amount, val in lastBet.items()]) # amount bet by opponent
                        diffSum = lastSum - prevSum # difference that still needs to be paid
                        diffDict = Chips.Chips().valueToChips(diffSum)
                        self.chips.betChips(diffDict, pot)
                    else:
                        self.chips.betChips(lastBet, pot)
                    self.decision = 'call'
                elif int(choice) == 2:
                    print("Your current total is " + str(self.chips.chips))
                    print("Enter ! to quit at anytime")

                    control = False
                    while control == False:
                        betsDict = {}
                        bet_value = ''
                        while True:
                            bet_value = str(input('What denomination would you like to bet: '))
                            if bet_value == '!':
                                break
                            bet_amount = int(input('How much of that denomination do you want to bet: '))

                            betsDict[bet_value] = bet_amount

                        if sum([int(amount) * val for amount, val in betsDict.items()]) <= numLastBet:
                            print("You can not raise less than the previous bet.")
                        else:
                            control = True

                    if self.prevBet != 0:
                        prevSum = sum([int(amount) * val for amount, val in self.prevBet.items()]) # previous amount raised by you
                        lastSum = sum([int(amount) * val for amount, val in betsDict.items()]) # amount bet by opponent
                        diffSum = lastSum - prevSum # difference that still needs to be paid
                        diffDict = Chips.Chips().valueToChips(diffSum)
                        self.chips.betChips(diffDict, pot)
                    else:
                        self.chips.betChips(betsDict, pot)
                    self.decision = 'raise'
                    return betsDict
                elif int(choice) == 3:
                    print()
                    print(self.chips)
                else:
                    self.decision = 'fold'
        return {'0' : 0}
            

class AIPlayer(Player):
    def __init__(self, id, hasht):
        super().__init__(id)
        self.hashTable = hasht


    def play(self, pot, lastBet, currBoard):
        numLastBet = sum([int(amount) * val for amount, val in lastBet.items()])

        input_data = np.array([[self.hashTable[str(card)] for card in self.hand] + [self.hashTable[str(card)] for card in currBoard]])

        predictions = pygad.nn.predict(last_layer=self.gann.population_networks[self.idx],
                                   data_inputs=input_data)
        choice = np.argmax(predictions)

        if choice == 0:
            self.decision = 'check'
        elif choice == 1:
            #AI BET MORE CHIPS IF HAND IS GOOD
            successfulBet = self.chips.betChips({'5': 1}, pot)
            if successfulBet:
                self.decision = 'bet'
            else:
                self.game_over = True
        elif choice == 2:
            self.decision = 'fold'

        return {'0': 0}
    def passParams(self, gann, idx):
        self.gann = gann
        self.idx = idx

class randomPlayer(Player):
    def __init__(self, id):
        super().__init__(id)

    def play(self, pot, lastBet, currBoard):
        
        choice = random.randint(0, 20)
        numLastBet = sum([int(amount) * val for amount, val in lastBet.items()])

        if choice > 0 and choice < 14:
            self.decision = 'check'
        elif choice >= 14 and choice < 19:
            successfulBet = self.chips.betChips({'5': random.randint(1,3)}, pot)
            if successfulBet:
                self.decision = 'bet'
            else:
                self.game_over = True
        elif choice > 19:
            self.decision = 'fold'
        return {'0': 0}