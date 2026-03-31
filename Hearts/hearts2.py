from dataclasses import dataclass
import random
from typing import List, Optional

@dataclass
class Card:
    suit: str
    rank : str

    def print (self):
        print(f"{self.rank} of {self.suit}")

class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        # Creating all 52 cards
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def displayAll(self) -> None:
        for card in self.cards:
            card.print()

    def draw(self) -> Optional[Card]:
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []

    def playCard(self) -> Optional[Card]:
        if len(self.hand) > 0:
            return self.hand.pop(0)
        return None

    def displayBySuit(self, suit: str) -> None:
        print(f"Cards in {suit}:")
        for card in self.hand:
            if card.suit == suit:
                card.print()

if __name__ == "__main__":
    # Create the deck
    my_deck = Deck()
    
    # Shuffle the deck
    my_deck.shuffle()
    
    # Display cards in the shuffled deck
    print("Shuffled Deck:")
    my_deck.displayAll()

    # Deal a player 13 cards
    player1 = Player("Alric")
    for i in range(13):
        new_card = my_deck.draw()
        if new_card:
            player1.hand.append(new_card)

    # For a player to play a card
    print(f"\n ({player1.name}) plays a card:")
    card_played = player1.playCard()
    if card_played:
        card_played.print()

    # For each suit to display the list of cards the player has in that suit
    print(f"""Cards grouped by suit for {player1.name}:""")
    player1.displayBySuit("Spades")
    player1.displayBySuit("Hearts")
    player1.displayBySuit("Diamonds")
    player1.displayBySuit("Clubs")
