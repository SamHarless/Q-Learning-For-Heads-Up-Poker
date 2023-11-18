from Card import Card
import random

class Deck(object):
    def __init__(self):
        self.cards = [Card(suit, value) for value in range(1,14) for suit in [0, 1, 2, 3]]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def __str__(self):
        cardAsStr = [card.name() for card in self.cards]
        return cardAsStr
    
    def drawTop(self):
        return self.cards.pop(0)
        

myDeck = Deck()
myDeck.shuffle()
print(myDeck.cards)
print(myDeck.draw_top())