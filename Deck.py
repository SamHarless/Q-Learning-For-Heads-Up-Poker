from Card import Card
import random

class Deck(object):
    def __init__(self):
        self.cards = [Card(suit, value) for value in range(1,14) for suit in ["Hearts", "Spades", "Clubs", "Diamonds"]]

    def shuffle(self):

        random.shuffle(self.cards)
        

myDeck = Deck()
myDeck.shuffle()
print(myDeck.cards)
print(myDeck.cards[0])