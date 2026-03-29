from dataclasses import dataclass
import random

@dataclass
class Card:
    suit: str
    rank : str

    def print (self):
        print(f"{self.rank} of {self.suit}")

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        # Creating all 52 cards
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def displayAll(self):
        for card in self.cards:
            card.print()

if __name__ == "__main__":
    # Create the deck
    my_deck = Deck()
    
    # Shuffle the deck
    my_deck.shuffle()
    
    # Display cards in the shuffled deck
    print("Shuffled Deck:")
    my_deck.displayAll()
