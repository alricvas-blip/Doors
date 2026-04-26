from dataclasses import dataclass
import random
from typing import List, Optional

# A dataclass to represent a single playing card with a suit and a rank.
@dataclass
class Card:
    suit: str
    rank: str

    # Calculates the numerical value of a card for comparison. Ace is high.
    def get_value(self) -> int:
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        return ranks.index(self.rank) + 2

    # Provides a user-friendly string representation of the card.
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Represents a standard 52-card deck.
class Deck:
    def __init__(self) -> None:
        # The list of cards in the deck.
        self.cards: List[Card] = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        # Loop through each suit and rank to create all 52 cards.
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    # Shuffles the deck randomly.
    def shuffle(self) -> None:
        random.shuffle(self.cards)

    # Draws a single card from the top of the deck.
    def draw(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []
        # Points accumulated in the current round.
        self.points_this_round: int = 0
        # Total score across all rounds.
        self.total_score: int = 0

    # Displays the player's hand, sorted by suit and rank.
    def display_hand(self):
        print(f"\n{self.name}'s hand:")
        # Sort hand for easier viewing by suit order then card value.
        self.hand.sort(key=lambda c: (["Clubs", "Diamonds", "Spades", "Hearts"].index(c.suit), c.get_value()))
        for i, card in enumerate(self.hand):
            print(f"[{i}] {card}")

    # Allows a player to choose a card to play, handling input and validation.
    def choose_card(self, lead_suit: Optional[str], is_first_trick: bool) -> Card:
        self.display_hand()
        # Determine which cards are legal to play.
        valid_cards = self.get_valid_cards(lead_suit, is_first_trick)
        
        while True:
            try:
                # Get player input for their card choice.
                choice = int(input(f"{self.name}, enter the number of the card you want to play: "))
                if 0 <= choice < len(self.hand):
                    selected_card = self.hand[choice]
                    # Check if the selected card is a valid move.
                    if selected_card in valid_cards:
                        return self.hand.pop(choice)
                    else:
                        print(f"Invalid play! You must follow suit if possible ({lead_suit}).")
                else:
                    print("Invalid number. Choose from the list.")
            except ValueError:
                print("Please enter a valid number.")

    # Determines the list of valid cards a player can play based on game rules.
    def get_valid_cards(self, lead_suit: Optional[str], is_first_trick: bool) -> List[Card]:
        # If the player is leading the trick.
        if not lead_suit:
            # Special rule: First trick of the game MUST lead with the 2 of Clubs.
            if is_first_trick:
                for card in self.hand:
                    if card.suit == "Clubs" and card.rank == "2":
                        return [card]
            # Otherwise, any card can be led.
            return self.hand

        # If following suit, find all cards of the lead suit.
        follow_suit_cards = [c for c in self.hand if c.suit == lead_suit]
        if follow_suit_cards:
            # Special rule: Cannot play point cards on the first trick.
            if is_first_trick:
                non_point_cards = [c for c in follow_suit_cards if not (c.suit == "Hearts" or (c.suit == "Spades" and c.rank == "Queen"))]
                return non_point_cards if non_point_cards else follow_suit_cards
            return follow_suit_cards
        
        # If player cannot follow suit, they can discard any card.
        if is_first_trick:
            # Cannot play point cards on the first trick, even when discarding.
            non_point_cards = [c for c in self.hand if not (c.suit == "Hearts" or (c.suit == "Spades" and c.rank == "Queen"))]
            return non_point_cards if non_point_cards else self.hand
            
        return self.hand # Can play any card if unable to follow suit.

    # Allows the player to select 3 cards to pass to another player.
    def choose_cards_to_pass(self) -> List[Card]:
        print(f"\n{self.name}: Choose 3 cards to pass.")
        self.display_hand()
        indices = []
        # Loop until 3 unique card indices are selected.
        while len(indices) < 3:
            try:
                choice = int(input(f"Card {len(indices)+1} index: "))
                if 0 <= choice < len(self.hand) and choice not in indices:
                    indices.append(choice)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Enter a number.")
        
        # Sort indices in reverse to pop from the end without messing up earlier indices.
        indices.sort(reverse=True)
        return [self.hand.pop(i) for i in indices]

# Manages the overall game flow of Hearts.
class HeartsGame:
    def __init__(self, names: List[str]):
        # Create Player objects from a list of names.
        self.players = [Player(name) for name in names]
        self.round_num = 1

    # Main game loop that continues until a player reaches 100 points.
    def play_game(self):
        while all(p.total_score < 100 for p in self.players):
            self.play_round()
            self.round_num += 1
        
        print("\n=== GAME OVER ===")
        winner = min(self.players, key=lambda p: p.total_score)
        # Find and announce the winner (player with the lowest score).
        for p in self.players:
            print(f"{p.name}: {p.total_score}")
        print(f"\nWINNER: {winner.name}!")

    # Manages the logic for a single round of Hearts (13 tricks).
    def play_round(self):
        print(f"\n***************************")
        print(f"*      HEARTS ROUND {self.round_num}     *")
        print(f"***************************")
        
        # Create and shuffle a new deck for the round.
        deck = Deck()
        deck.shuffle()
        # Deal 13 cards to each player.
        for _ in range(13):
            for p in self.players:
                p.hand.append(deck.draw())
        
        # Passing Phase
        # Execute the card passing phase.
        self.passing_phase()

        # Determine who starts (has 2 of Clubs)
        # Determine who starts the first trick (player with the 2 of Clubs).
        leader_idx = 0
        for i, p in enumerate(self.players):
            if any(c.suit == "Clubs" and c.rank == "2" for c in p.hand):
                leader_idx = i
                break

        # Play 13 tricks
        # Play 13 tricks to complete the round.
        for t in range(1, 14):
            leader_idx = self.play_trick(t, leader_idx)

        # Scoring
        # After all tricks, tally scores for the round.
        for p in self.players:
            p.total_score += p.points_this_round
            print(f"{p.name} earned {p.points_this_round} pts. Total: {p.total_score}")
            p.points_this_round = 0 # Reset round points for the next round.

    # Manages the passing of 3 cards between players at the start of a round.
    def passing_phase(self):
        # Passing direction changes each round: Left, Right, Across, then None.
        direction = (self.round_num - 1) % 4
        if direction == 3: # Fourth round has no passing.
            print("No passing this round.")
            return

        # Each player chooses 3 cards to pass.
        all_passed = [p.choose_cards_to_pass() for p in self.players]
        # Offsets determine passing direction: 1=Left, -1=Right, 2=Across.
        offsets = [1, -1, 2] # Left, Right, Across
        offset = offsets[direction]
        
        # Distribute the passed cards to the correct players.
        for i in range(4):
            receiver = (i + offset) % 4
            self.players[receiver].hand.extend(all_passed[i])
        print("Passing complete.")

    # Manages the logic for a single trick (one card played by each player).
    def play_trick(self, trick_num, leader_idx) -> int:
        print(f"\n--- TRICK {trick_num} ---")
        # Cards played in this trick.
        trick_cards = []
        # The order of players in this trick.
        played_order = []
        
        # Leading
        # The leader of the trick plays a card.
        p = self.players[leader_idx]
        card = p.choose_card(None, trick_num == 1)
        print(f"{p.name} leads with {card}")
        trick_cards.append(card)
        played_order.append(leader_idx)
        lead_suit = card.suit

        # Others play
        # The other 3 players play their cards in order.
        for i in range(1, 4):
            curr_idx = (leader_idx + i) % 4
            p = self.players[curr_idx]
            card = p.choose_card(lead_suit, trick_num == 1)
            print(f"{p.name} plays {card}")
            trick_cards.append(card)
            played_order.append(curr_idx)

        # Determine winner
        # Determine the winner of the trick (highest card of the lead suit).
        highest_val = -1
        winner_idx_in_trick = 0
        for i, card in enumerate(trick_cards):
            if card.suit == lead_suit and card.get_value() > highest_val:
                highest_val = card.get_value()
                winner_idx_in_trick = i
        
        # Get the index of the player who won.
        winner_actual_idx = played_order[winner_idx_in_trick]
        winner = self.players[winner_actual_idx]
        
        # Calculate points
        # Calculate points in the trick (1 for each Heart, 13 for Queen of Spades).
        points = sum(1 for c in trick_cards if c.suit == "Hearts")
        if any(c.suit == "Spades" and c.rank == "Queen" for c in trick_cards):
            points += 13
            
        # Assign points to the trick winner.
        winner.points_this_round += points
        print(f"*** {winner.name} wins the trick ({points} points)! ***")
        # The winner of the trick leads the next trick.
        return winner_actual_idx

# Main execution block.
if __name__ == "__main__":
    # Create and start a new game with 4 players.
    game = HeartsGame(["Alric", "Bot 1", "Bot 2", "Bot 3"])
    game.play_game()
