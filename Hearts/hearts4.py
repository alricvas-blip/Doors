# hearts4.py
# A professional and complete version of the Hearts card game.
# This code adheres to basic Python syntax (for/while loops, if/else statements)
# as per the assignment's requirements, avoiding advanced features like
# list comprehensions, lambda, enumerate, or any.

import random
from typing import List, Optional

# A helper function to get a sorting key for a card.
# This replaces the need for a lambda function in sorting.
def get_card_sort_key(card):
    """Returns a tuple used for sorting cards by suit, then rank."""
    suit_order = ["Clubs", "Diamonds", "Spades", "Hearts"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    return (suit_order.index(card.suit), ranks.index(card.rank))

class Card:
    """Represents a single playing card."""
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        """Provides a user-friendly string representation of the card."""
        return f"{self.rank} of {self.suit}"

class Deck:
    """Represents a standard 52-card deck."""
    def __init__(self) -> None:
        self.cards: List[Card] = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Pile:
    """Represents the pile of cards played in a single trick."""
    def __init__(self):
        # This list will hold tuples of (card, player_who_played_it).
        self.cards_in_pile: List = []

    def add_card(self, card: Card, player):
        """Adds a card to the pile."""
        self.cards_in_pile.append((card, player))

    def get_lead_card(self) -> Optional[Card]:
        """Returns the first card played in the trick."""
        if len(self.cards_in_pile) > 0:
            return self.cards_in_pile[0][0]
        return None

    def clear(self) -> List[Card]:
        """Clears the pile and returns the cards that were in it."""
        cards = []
        for item in self.cards_in_pile:
            cards.append(item[0])
        self.cards_in_pile = []
        return cards

class Player:
    """Represents a player, holding a hand and managing scores."""
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: List[Card] = []
        self.captured_cards: List[Card] = []
        self.round_score: int = 0
        self.total_score: int = 0

    def display_hand(self):
        """Displays the player's hand, sorted for readability."""
        print(f"\n{self.name}'s hand:")
        self.hand.sort(key=get_card_sort_key)
        
        # A standard for-loop to print cards with an index, replacing enumerate().
        i = 0
        while i < len(self.hand):
            print(f"[{i}] {self.hand[i]}")
            i += 1

    def get_valid_cards(self, lead_suit: Optional[str], hearts_broken: bool) -> List[Card]:
        """Determines the list of valid cards a player can legally play."""
        # If player is leading the trick
        if lead_suit is None:
            # Check if player must lead a heart because it's all they have
            only_has_hearts = True
            for card in self.hand:
                if card.suit != "Hearts":
                    only_has_hearts = False
                    break
            
            # If hearts are broken or player only has hearts, any card is valid
            if hearts_broken or only_has_hearts:
                return self.hand
            else:
                # Otherwise, cannot lead with a heart
                valid_cards = []
                for card in self.hand:
                    if card.suit != "Hearts":
                        valid_cards.append(card)
                return valid_cards
        
        # If player is following suit
        valid_cards = []
        for card in self.hand:
            if card.suit == lead_suit:
                valid_cards.append(card)
        
        # If player has cards of the lead suit, they must play one
        if len(valid_cards) > 0:
            return valid_cards
        else:
            # If they cannot follow suit, they can play any card
            return self.hand

    def choose_card_to_play(self, lead_suit: Optional[str], hearts_broken: bool, is_first_trick: bool) -> Card:
        """Asks the player to choose a valid card to play."""
        self.display_hand()
        
        # On the first trick, the 2 of Clubs must be played
        if is_first_trick:
            for card in self.hand:
                if card.suit == "Clubs" and card.rank == "2":
                    print(f"{self.name} must lead with the 2 of Clubs.")
                    self.hand.remove(card)
                    return card

        valid_cards = self.get_valid_cards(lead_suit, hearts_broken)
        
        while True:
            try:
                choice = int(input(f"{self.name}, enter the number of the card to play: "))
                if 0 <= choice < len(self.hand):
                    selected_card = self.hand[choice]
                    if selected_card in valid_cards:
                        self.hand.pop(choice)
                        return selected_card
                    else:
                        print("Invalid move. You must follow suit or obey lead rules.")
                else:
                    print("Invalid number. Please choose from your hand.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number.")

    def choose_cards_to_pass(self) -> List[Card]:
        """Asks the player to choose 3 cards to pass."""
        self.display_hand()
        print(f"\n{self.name}: Choose 3 cards to pass.")
        indices = []
        while len(indices) < 3:
            try:
                choice = int(input(f"Choose card {len(indices) + 1} of 3 (by number): "))
                # Check if choice is valid and not already chosen
                is_valid = False
                if 0 <= choice < len(self.hand):
                    is_in_indices = False
                    for i in indices:
                        if i == choice:
                            is_in_indices = True
                            break
                    if not is_in_indices:
                        indices.append(choice)
                        is_valid = True

                if not is_valid:
                    print("Invalid or duplicate selection.")
            except ValueError:
                print("Please enter a number.")
        
        indices.sort(reverse=True)
        # Use a for loop to build the list of cards to pass
        cards_to_pass = []
        for index in indices:
            cards_to_pass.append(self.hand.pop(index))
        return cards_to_pass

    def calculate_round_score(self):
        """Calculates score for the round from captured cards."""
        self.round_score = 0
        for card in self.captured_cards:
            if card.suit == "Hearts":
                self.round_score += 1
            if card.suit == "Spades" and card.rank == "Queen":
                self.round_score += 13

class HeartsGame:
    """Manages the complete game flow, from setup to winner declaration."""
    def __init__(self, names: List[str]):
        # Use a for loop to create players, replacing the list comprehension
        self.players: List[Player] = []
        for name in names:
            self.players.append(Player(name))
        
        self.pile = Pile()
        self.round_num = 0
        self.hearts_broken = False

    def play_game(self):
        """Main game loop that continues until a player's score reaches 100."""
        while True:
            # Check if any player has reached 100 points
            game_over = False
            for p in self.players:
                if p.total_score >= 100:
                    game_over = True
                    break
            if game_over:
                break
            
            self.play_round()
        
        # Find and announce the winner (player with the lowest score)
        print("\n=== GAME OVER ===")
        winner = self.players[0]
        for p in self.players:
            if p.total_score < winner.total_score:
                winner = p
        
        for p in self.players:
            print(f"Final Score for {p.name}: {p.total_score}")
        print(f"\nWINNER: {winner.name}!")

    def play_round(self):
        """Manages the logic for a single round of Hearts (13 tricks)."""
        self.round_num += 1
        print(f"\n***************************\n*      HEARTS ROUND {self.round_num}     *\n***************************")
        
        # --- Setup Phase ---
        self.hearts_broken = False
        deck = Deck()
        deck.shuffle()
        for p in self.players:
            p.hand = []
            p.captured_cards = []
            p.round_score = 0
        
        for _ in range(13):
            for p in self.players:
                p.hand.append(deck.draw())
        
        # --- Passing Phase ---
        self.passing_phase()

        # --- Trick-Playing Phase ---
        # Find the player with the 2 of Clubs to lead the first trick
        leader_idx = 0
        found_leader = False
        for i in range(len(self.players)):
            for card in self.players[i].hand:
                if card.suit == "Clubs" and card.rank == "2":
                    leader_idx = i
                    found_leader = True
                    break
            if found_leader:
                break

        # Play 13 tricks
        for i in range(13):
            print(f"\n--- Trick {i + 1} of 13 ---")
            leader_idx = self.play_trick(leader_idx, i == 0)
        
        # --- Scoring Phase ---
        self.tally_scores()

    def passing_phase(self):
        """Manages passing 3 cards based on the round number."""
        direction = (self.round_num - 1) % 4
        if direction == 3: # Fourth round: no passing
            print("No passing this round.")
            return

        pass_directions = ["Left", "Right", "Across"]
        print(f"Passing direction: {pass_directions[direction]}")
        
        # Use a for loop to collect cards to pass, replacing list comprehension
        all_passed = []
        for p in self.players:
            all_passed.append(p.choose_cards_to_pass())
        
        # Distribute the passed cards to the correct players
        for i in range(4):
            cards_from_player_i = all_passed[i]
            receiver_idx = i
            if direction == 0: # Pass Left
                receiver_idx = (i + 1) % 4
            elif direction == 1: # Pass Right
                receiver_idx = (i - 1 + 4) % 4
            elif direction == 2: # Pass Across
                receiver_idx = (i + 2) % 4
            
            self.players[receiver_idx].hand.extend(cards_from_player_i)

    def play_trick(self, leader_idx: int, is_first_trick: bool) -> int:
        """Manages the logic for a single trick."""
        lead_suit = None
        
        # The 4 players play their cards in order
        for i in range(4):
            current_player_idx = (leader_idx + i) % 4
            player = self.players[current_player_idx]
            
            card = player.choose_card_to_play(lead_suit, self.hearts_broken, is_first_trick)
            print(f"{player.name} plays {card}")
            
            if not self.hearts_broken and card.suit == "Hearts":
                self.hearts_broken = True
                print("!!! Hearts have been broken! !!!")

            if i == 0:
                lead_suit = card.suit
            
            self.pile.add_card(card, player)

        # Determine the winner of the trick
        winning_card, winner = self.pile.cards_in_pile[0]
        for card, player in self.pile.cards_in_pile:
            if card.suit == lead_suit:
                ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
                if ranks.index(card.rank) > ranks.index(winning_card.rank):
                    winning_card = card
                    winner = player
        
        print(f"*** {winner.name} wins the trick! ***")
        
        # Winner captures the cards from the pile
        captured = self.pile.clear()
        winner.captured_cards.extend(captured)
        
        # Return the winner's index to lead the next trick
        winner_index = self.players.index(winner)
        return winner_index

    def tally_scores(self):
        """Calculates and applies scores, checking for Shooting the Moon."""
        for p in self.players:
            p.calculate_round_score()
        
        # Check if any player shot the moon
        moon_shooter = None
        for p in self.players:
            if p.round_score == 26:
                moon_shooter = p
                break
        
        print("\n--- End of Round Scores ---")
        if moon_shooter:
            print(f"!!! {moon_shooter.name} has SHOT THE MOON! !!!")
            for p in self.players:
                if p is moon_shooter:
                    p.round_score = 0
                else:
                    p.round_score = 26
        
        # Add round scores to total scores
        for p in self.players:
            p.total_score += p.round_score
            print(f"{p.name}: +{p.round_score} points. Total: {p.total_score}")

if __name__ == "__main__":
    game = HeartsGame(["Alric", "Bot 1", "Bot 2", "Bot 3"])
    game.play_game()
