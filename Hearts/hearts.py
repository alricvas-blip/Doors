import random
class Card:
    def __init__(self, r, s):
        self.rank = r
        self.suit = s
class Deck:
    def __init__(self):
        self.cards = []
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "King", "Jack", "Queen"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for s in suits:
            for r in ranks:
                new_card = Card(r, s)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for card in self.cards:
            print(card.rank + " of " + card.suit)
my_deck = Deck()
my_deck.shuffle()
my_deck.show()