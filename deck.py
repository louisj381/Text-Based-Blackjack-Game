from random import choice
from random import shuffle

class Deck:
    values = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    ten_valued_cards = values[-4:]
    suits = ['D', 'S', 'C', 'H']
    def __init__(self):
        cards = []
        for suit in self.suits:
            for value in self.values:
                cards.append((value, suit))
        self.cards = cards

    def getRandomCard(self):
        shuffle(self.cards)
        return choice(self.cards)

class Hand:
    def __init__(self, money = 100):
        self.money = money
        self.cards = []
        self.bet = 0

    #methods
    def addCard(self, card):
        self.cards.append(card)
        # print("this object (" + str(self) + ") has cards: " + str(self.cards))

    def emptyHand(self):
        self.cards.clear()

    def clearBet(self):
        self.bet = 0

    def getBet(self):
        return self.bet

    def getBestValue(self):
        total_value = 0
        has_ace = False
        for (value, _) in self.cards:
            if value == 'A':
                total_value += 1
                has_ace = True
            elif value in Deck.ten_valued_cards:
                total_value += 10
            else:
                total_value += value
        if has_ace and total_value + 10 <= 21:
            total_value += 10
        return total_value

    def setBet(self, amount):
        if amount >= self.money:
            print("all in!")
            all_money = self.money
            self.bet = all_money
            self.money = 0
        else:
            self.money -= amount
            self.bet += amount

    #expects the actual amount player bet
    def win(self, amount):
        amount *=2 #winning means you get double!
        self.money += amount

    def print_cards(self, whose="your"):
        print(str(whose) + " cards:")
        for card in self.cards:
            print(str(card))
