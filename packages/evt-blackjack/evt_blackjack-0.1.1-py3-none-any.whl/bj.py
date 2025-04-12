#!/usr/bin/env python3
import random
from typing import List

class Card:
    # ANSI color codes
    RED = '\033[91m'
    BLACK = '\033[90m'
    RESET = '\033[0m'

    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value
        self.color = self.RED if suit in ['Hearts', 'Diamonds'] else self.BLACK

    def display(self) -> str:
        suit_symbols = {
            "Spades": "♠",
            "Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣"
        }
        symbol = suit_symbols.get(self.suit, "?")
        val = self.value[0] if self.value != "10" else "10"

        top = f"┌─────────┐"
        mid1 = f"│{self.color}{val:<2}{self.RESET}       │"
        mid2 = f"│         │"
        mid3 = f"│    {self.color}{symbol}{self.RESET}    │"
        mid4 = f"│         │"
        mid5 = f"│       {self.color}{val:>2}{self.RESET}│"
        bot = f"└─────────┘"
        
        return "\n".join([top, mid1, mid2, mid3, mid4, mid5, bot])

    @staticmethod
    def blank_display() -> str:
        top = f"┌─────────┐"
        mid1 = f"│         │"
        mid2 = f"│         │"
        mid3 = f"│    ?    │"
        mid4 = f"│         │"
        mid5 = f"│         │"
        bot = f"└─────────┘"
        
        return "\n".join([top, mid1, mid2, mid3, mid4, mid5, bot])

    def __str__(self) -> str:
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self, num_decks: int = 6, shuffle_threshold: int = 20):
        self.num_decks = num_decks
        self.shuffle_threshold = shuffle_threshold
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        
        self.cards = []
        for _ in range(self.num_decks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(suit, value))
        self.shuffle()

    def shuffle(self) -> None:
        print("\nDealer is shuffling the cards...")
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if len(self.cards) <= self.shuffle_threshold:
            print(f"\nOnly {len(self.cards)} cards remaining. Reshuffling deck...")
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def display(self, hide_second: bool = False) -> str:
        if not self.cards:
            return ""
        
        if hide_second and len(self.cards) > 1:
            # Get the display lines for visible cards
            visible_cards = [self.cards[0].display().split('\n')]
            # Add blank card for hidden card
            visible_cards.append(Card.blank_display().split('\n'))
            
            # Combine the lines horizontally
            result = []
            for i in range(7):  # Each card has 7 lines
                line = "  ".join(card[i] for card in visible_cards)
                result.append(line)
            
            return "\n".join(result)
        else:
            # Get the display lines for each card
            card_displays = [card.display().split('\n') for card in self.cards]
            
            # Combine the lines horizontally
            result = []
            for i in range(7):  # Each card has 7 lines
                line = "  ".join(card[i] for card in card_displays)
                result.append(line)
            
            return "\n".join(result)

    def is_blackjack(self) -> bool:
        if len(self.cards) != 2:
            return False
        has_ace = any(card.value == 'Ace' for card in self.cards)
        has_ten = any(card.value in ['10', 'Jack', 'Queen', 'King'] for card in self.cards)
        return has_ace and has_ten

    def get_value(self) -> int:
        value = 0
        num_aces = 0
        
        for card in self.cards:
            if card.value in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.value == 'Ace':
                num_aces += 1
            else:
                value += int(card.value)
        
        # Add aces
        for _ in range(num_aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
                
        return value

    def get_value_with_ace(self) -> str:
        value = 0
        num_aces = 0
        
        for card in self.cards:
            if card.value in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.value == 'Ace':
                num_aces += 1
            else:
                value += int(card.value)
        
        if num_aces == 0:
            return str(value)
        
        # Calculate both possible values with aces
        low_value = value + num_aces  # All aces as 1
        high_value = value + (11 * num_aces)  # All aces as 11
        
        if high_value > 21:
            return str(low_value)
        return f"{high_value} / {low_value}"

    def __str__(self) -> str:
        return ', '.join(str(card) for card in self.cards)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.player_balance = 0
        self.current_bet = 0
        self.hand_count = 0

    def get_starting_balance(self) -> None:
        while True:
            try:
                balance = float(input("\nEnter your starting balance: $"))
                if balance > 0:
                    self.player_balance = balance
                    break
                print("Please enter a positive amount.")
            except ValueError:
                print("Please enter a valid number.")

    def get_bet(self) -> None:
        while True:
            try:
                print(f"\nYour current balance: ${self.player_balance:.2f}")
                bet = float(input("Enter your bet amount: $"))
                if bet <= 0:
                    print("Bet must be greater than 0.")
                elif bet > self.player_balance:
                    print("You don't have enough money for that bet.")
                else:
                    self.current_bet = bet
                    self.player_balance -= bet
                    break
            except ValueError:
                print("Please enter a valid number.")

    def deal_initial_cards(self) -> None:
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

    def player_turn(self) -> None:
        # Check for double down opportunity after initial cards
        if len(self.player_hand.cards) == 2 and self.player_balance >= self.current_bet:
            while True:
                action = input("\nWould you like to (h)it, (s)tand, or (d)ouble down? ").lower()
                if action == 'd':
                    self.player_balance -= self.current_bet
                    self.current_bet *= 2
                    print(f"\nDoubling down! New bet: ${self.current_bet:.2f}")
                    drawn_card = self.deck.draw()
                    self.player_hand.add_card(drawn_card)
                    print(f"You drew:")
                    print(drawn_card.display())
                    print(f"Your total: {self.player_hand.get_value_with_ace()}")
                    if self.player_hand.get_value() > 21:
                        print("Bust! You lose!")
                        self.game_over = True
                    return
                elif action == 's':
                    return
                elif action == 'h':
                    drawn_card = self.deck.draw()
                    self.player_hand.add_card(drawn_card)
                    print(f"You drew:")
                    print(drawn_card.display())
                    print(f"Your total: {self.player_hand.get_value_with_ace()}")
                    if self.player_hand.get_value() > 21:
                        print("Bust! You lose!")
                        self.game_over = True
                        return
                    break
                else:
                    print("Invalid input. Please enter 'h' for hit, 's' for stand, or 'd' for double down.")

        while True:
            if self.player_hand.get_value() > 21:
                print("Bust! You lose!")
                self.game_over = True
                return

            action = input("\nWould you like to (h)it or (s)tand? ").lower()
            if action == 'h':
                drawn_card = self.deck.draw()
                self.player_hand.add_card(drawn_card)
                print(f"You drew:")
                print(drawn_card.display())
                print(f"Your total: {self.player_hand.get_value_with_ace()}")
                if self.player_hand.get_value() > 21:
                    print("Bust! You lose!")
                    self.game_over = True
                    return
            elif action == 's':
                break
            else:
                print("Invalid input. Please enter 'h' for hit or 's' for stand.")

    def dealer_turn(self) -> None:
        print(f"\nDealer's hand:")
        print(self.dealer_hand.display())
        while self.dealer_hand.get_value() < 17:
            drawn_card = self.deck.draw()
            self.dealer_hand.add_card(drawn_card)
            print(f"Dealer draws:")
            print(drawn_card.display())
            print(f"Dealer's total: {self.dealer_hand.get_value_with_ace()}")

    def determine_winner(self) -> None:
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()

        print(f"\nYour total: {self.player_hand.get_value_with_ace()}")
        print(f"Dealer's total: {self.dealer_hand.get_value_with_ace()}")

        if player_value > 21:
            print("You bust! Dealer wins!")
        elif dealer_value > 21:
            print(f"Dealer busts! You win! +${self.current_bet * 2:.2f}")
            self.player_balance += self.current_bet * 2
        elif player_value > dealer_value:
            print(f"You win! +${self.current_bet * 2:.2f}")
            self.player_balance += self.current_bet * 2
        elif dealer_value > player_value:
            print("Dealer wins!")
        else:
            print("It's a tie!")
            self.player_balance += self.current_bet

        print(f"Current balance: ${self.player_balance:.2f}")

    def play(self) -> None:
        print("\nWelcome to Blackjack!")
        self.get_starting_balance()
        
        while True:
            if self.player_balance <= 0:
                print("\nYou're out of money! Game over.")
                break
            
            self.hand_count += 1
            print("\n" + "_" * 10)
            print(f"HAND {self.hand_count}")
            print("_" * 10)
            
            # Reset for new hand
            self.game_over = False
            self.player_hand = Hand()
            self.dealer_hand = Hand()
                
            self.get_bet()
            self.deal_initial_cards()
            
            print(f"\nDealer's hand:")
            print(self.dealer_hand.display(hide_second=True))
            print(f"\nYour hand:")
            print(self.player_hand.display())
            print(f"Your total: {self.player_hand.get_value_with_ace()}")

            # Check for blackjacks
            if self.dealer_hand.is_blackjack():
                print("\nDealer reveals their hand:")
                print(self.dealer_hand.display())
                print("\nDEALER BLACKJACK!")
                if self.player_hand.is_blackjack():
                    print("You also have Blackjack! Push!")
                    self.player_balance += self.current_bet
                self.game_over = True
            elif self.player_hand.is_blackjack():
                print("\nDealer reveals their hand:")
                print(self.dealer_hand.display())
                blackjack_payout = self.current_bet + (self.current_bet * 1.5)
                print(f"\nBLACKJACK! +${blackjack_payout:.2f}")
                self.player_balance += blackjack_payout
                self.game_over = True
            
            if not self.game_over:
                self.player_turn()
                
                if not self.game_over:
                    print("\nDealer reveals their hand:")
                    print(self.dealer_hand.display())
                    self.dealer_turn()
                    self.determine_winner()
                else:
                    print("\nDealer reveals their hand:")
                    print(self.dealer_hand.display())
                    print(f"Dealer's total: {self.dealer_hand.get_value_with_ace()}")
            
            while True:
                play_again = input("\nWould you like to play again? (y/n): ").lower()
                if play_again in ['y', 'n']:
                    break
                print("Please enter 'y' for yes or 'n' for no.")
            
            if play_again != 'y':
                break

def main():
    game = BlackjackGame()
    game.play()

if __name__ == "__main__":
    main()