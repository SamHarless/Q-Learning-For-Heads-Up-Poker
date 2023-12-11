import Card
import Pot

# Constants for hand types
HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8
ROYAL_FLUSH = 9

class Hand:
    def __init__(self, players, deck, bigBlind):
        self.players = players
        self.deck = deck
        self.bigBlind = bigBlind
        self.pot = Pot.Pot()
        self.board = [Card.Card(-1,-1), Card.Card(-1,-1), Card.Card(-1,-1), Card.Card(-1,-1), Card.Card(-1,-1)]

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
    
    def evaluate_hand(self, cards):
        """
        Evaluate a poker hand using a bitwise representation.
        Returns a tuple (hand_type, hand_value).
        """
        values = sorted([card.value for card in cards], reverse=True)

        

        # flush
        is_flush = len(set([card.suit for card in cards])) == 1

        # straight
        is_straight = values[0] - values[4] == 4 and len(set(values)) == 5

        # royal
        is_royal_flush = is_straight and is_flush and values[0] == 14

        # four of a kind, full house, three of a kind, two pair, or one pair
        value_counts = [values.count(value) for value in set(values)]

        # Check for four of a kind, full house, three of a kind, two pair, or one pair
        hand_type = max(value_counts)
        if hand_type == 4:
            return (FOUR_OF_A_KIND, values[0])
        elif hand_type == 3:
            if 2 in value_counts:
                return (FULL_HOUSE, (values[0], values[-1]))
            else:
                return (THREE_OF_A_KIND, values[0])
        elif hand_type == 2:
            if value_counts.count(2) == 2:
                return (TWO_PAIR, (values[0], values[-1], values[1]))
            else:
                return (ONE_PAIR, (values[0], values[2], values[3], values[4]))

        # Check for straight flush or flush
        if is_royal_flush:
            return (ROYAL_FLUSH,)
        if is_straight and is_flush:
            return (STRAIGHT_FLUSH, values[0])
        elif is_flush:
            return (FLUSH, values[0])

        # Check for straight or high card
        if is_straight:
            return (STRAIGHT, values[0])

        return (HIGH_CARD, tuple(values))
    
    def compareHands(self):
        """
        Compare two poker hands and return 1 if hand1 is better, -1 if hand2 is better, and 0 if they are tied.
        """
        tempBoard = self.board
        tempBoard.extend(self.players[0].hand)
        type1, value1 = self.evaluate_hand(tempBoard)

        tempBoard = self.board
        tempBoard.extend(self.players[1].hand)
        type2, value2 = self.evaluate_hand(tempBoard)

        if type1 > type2:
            return 0
        elif type1 < type2:
            return 1
        else:
            # Compare values within the same hand type
            if type1 in {HIGH_CARD, STRAIGHT, FLUSH, STRAIGHT_FLUSH, ROYAL_FLUSH}:
                for v1, v2 in zip(value1, value2):
                    if v1 > v2:
                        return 0
                    elif v1 < v2:
                        return 1
            else:
                if value1 > value2:
                    return 0
                elif value1 < value2:
                    return 1

        return -1

    def fillWithZeros(self, list):

        if len(list) > 10:
            return list[-10:]
        
        while len(list) < 10:
            list.append(0)
        return list
    
    def startHand(self, verbose=False):
        #print("START HAND")
        # get big blind from player
        self.players[self.bigBlind].chips.bigBlind(self.pot)
        # deal cards
        self.players[self.bigBlind].assignHand(self.deck)
        self.players[int(not self.bigBlind)].assignHand(self.deck)

        self.history = []

        fold = False
        i = 0
        while i < 4 and fold == False:
            for player in self.players: player.resetDecision()

            currentPlayer = int(not self.bigBlind) # big blind plays last
            lastBet = {'5' : 1} if i == 0 else {'0' : 0}
            # print("\n\n\n\n\n\n\n")
            if verbose: print("The current board is: " + str(self.showBoard())) #comment out for train

            while self.decisionsMade() == False:
                if verbose: print("Current Player is " + str(currentPlayer)) #comment out for train
                lastBet = self.players[currentPlayer].play(self.pot, lastBet, self.showBoard(), verbose, self.fillWithZeros(self.history))

                if len(lastBet) !=0:
                    if sum([int(amount) * val for amount, val in lastBet.items()]) != 0:
                        self.history.append(sum([int(amount) * val for amount, val in lastBet.items()]))

                if self.players[currentPlayer].decision == 'fold':
                    fold = True
                    break
                elif self.players[currentPlayer].decision == 'bet' or self.players[currentPlayer].decision == 'raise':
                    self.players[currentPlayer].prevBet = lastBet
                    self.players[int(not currentPlayer)].decision = None
                    currentPlayer = int(not currentPlayer)
                else:
                    currentPlayer = int(not currentPlayer)
            # board for the cards
            # win logic
            if fold == True: 
                break

            if i == 0:
                burn = self.deck.drawTop()
                self.board[0] = self.deck.drawTop()
                self.board[1] = self.deck.drawTop()
                self.board[2] = self.deck.drawTop()
            elif i != 3:
                burn = self.deck.drawTop()
                self.board[i+2] = self.deck.drawTop()
            i+=1

        # reward pot to non-folder
        if fold == True:
            for player in self.players:
                if player.decision != 'fold':
                    potValue = self.pot.getValue()
                    chipDict = player.chips.valueToChips(potValue)
                    player.chips.addChips(chipDict)

        # reward pot to winner
        winner = self.compareHands()
        # tie
        if winner == -1:
            potValue = self.pot.getValue()
            potValueHalf = self.pot.getValue() // 2

            remain = potValueHalf % int(self.players[0].chips.lowestDenom)

            if remain != 0:
                potValueHalf = potValueHalf - remain
                morePotValueHalf = potValue - potValueHalf
            else:
                morePotValueHalf = potValueHalf

            #player 0 gets the lesser half
            chipDict = self.players[0].chips.valueToChips(potValueHalf)
            self.players[0].chips.addChips(chipDict)

            #player 
            chipDict = self.players[1].chips.valueToChips(morePotValueHalf)
            self.players[1].chips.addChips(chipDict)
            if verbose: print("\nTie! The pot was chopped!")
        else:
            potValue = self.pot.getValue()
            chipDict = self.players[winner].chips.valueToChips(potValue)
            self.players[winner].chips.addChips(chipDict)
            if verbose: print("\nPlayer " + str(winner) + " won the hand! The pot was worth " + str(potValue))
        

        

                    


