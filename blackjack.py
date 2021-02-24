import random
import sys
import copy

"""
This is a small command line blackjack game that I wrote to get my feet wet in Python.
"""


# Represents a playing card
class Card:

    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def get_suit(self):
        return self.suit

    def get_val(self):
        return self.val


# Represents a deck of playing cards
class Deck:

    suits = ("Hearts", "Clubs", "Diamonds", "Spades")
    special = ("Jack", "Queen", "King")

    # Loops through each suit and creates a card of each value
    def __init__(self):
        self.cards = [None] * 52
        self.top = 0
        i = 0
        for suit in self.suits:
            c = Card(suit, "Ace")
            self.cards[i] = c
            i += 1
            for val in range(2, 11):
                c = Card(suit, val)
                self.cards[i] = c
                i += 1
            for s in self.special:
                c = Card(suit, s)
                self.cards[i] = c
                i += 1

    # Shuffle the deck
    def shuffle(self):
        shuffled = [None] * 52
        for card in self.cards:
            position = random.randrange(0, 52)
            while shuffled[position] is not None:
                position = random.randrange(0, 52)
            shuffled[position] = card
        self.cards = shuffled

    # Draw a card
    def draw(self):
        if self.top == 52:
            return
        helper = copy.deepcopy(self.top)
        self.top += 1
        return self.cards[helper]

    def print_all(self):
        for card in self.cards:
            print(card.get_suit() + " " + str(card.get_val()))


# Represents a player
class Player:

    def __init__(self, name, cards=None):
        self.score = 0
        self.name = name
        if cards is None:
            self.cards = []

    # Give the player another card
    def hit(self, c):
        if c.get_val() == "Ace":
            i = input("You drew an ace! Play as a 1 or 11?")
            self.score += int(i)
        elif c.get_val() == "Jack" or c.get_val() == "Queen" or c.get_val() == "King":
            self.score += 10
        else:
            self.score += int(c.get_val())
        self.cards.append(c)

    # Discard the player's hand
    def discard_hand(self):
        self.score = 0
        self.cards.clear()

    def get_score(self):
        return self.score

    def get_hand(self):
        return self.cards

    def get_name(self):
        return self.name

    def show_hand(self):
        for card in self.cards:
            print(str(card.get_suit()) + " " + str(card.get_val()))

    def in_hand(self, c):
        for card in self.cards:
            if c.get_val() == card.get_val() and c.get_suit() == card.get_suit():
                return True
        return False


# The class where the game is played
class BlackJack:

    def __init__(self, num, players=None, matches_won=None):
        if int(num) < 2:
            raise Exception("There must be 2 or more players")
        if players is None:
            players = [None] * int(num)
        if matches_won is None:
            matches_won = {}
        self.deck = Deck()
        self.deck.shuffle()
        for i in range(0, int(num)):
            name = input("Enter player " + str(i + 1) + "'s name: ")
            players[i] = Player(name)
            players[i].hit(self.deck.draw())
            players[i].hit(self.deck.draw())
            matches_won[name] = 0
        self.players = players
        self.matches_won = matches_won.copy()

    # One player takes his/her turn
    def turn(self, player):
        print(player.get_name() + "'s turn!")
        print("Here are your cards!")
        player.show_hand()
        while player.get_score() < 21:
            hit = input("Hit? <Y>")
            if hit.lower() == 'y':
                c = self.deck.draw()
                print("You draw: " + c.get_suit() + " " + str(c.get_val()))
                player.hit(c)
            if hit.lower() != 'y':
                break
        if player.get_score() == 21:
            print("Congratulations, you won!")
            self.matches_won[player.get_name()] += 1
            return True
        if player.get_score() > 21:
            print("You lose!")
        return False

    # Reset the game
    def reset(self):
        for player in self.players:
            player.discard_hand()
            player.hit(self.deck.draw())
            player.hit(self.deck.draw())

    # Run one match
    def match(self):
        for player in self.players:
            if self.turn(player):
                return
        winner = None
        high_score = -1
        for player in self.players:
            if 21 > player.get_score() > high_score:
                high_score = player.get_score()
                winner = player.get_name()
        if winner is not None:
            self.matches_won[winner] += 1
            print("Congratulations, " + winner + " you won!")
        else:
            print("No one won this round!")
        return winner
    
    # Find who won the whole game
    def find_winner(self):
        points = -1
        for name, score in self.matches_won.items():
            if score > points:
                points = score
        for player in self.players:
            if player.get_score() == points:
                print("Congratulations " + player.get_name() + ", you won")
        return

    def game(self, rounds):
        for i in range(0, int(rounds)):
            self.match()
            self.reset()
        self.find_winner()


def main():
    print("Welcome to blackjack!")
    num = input("How many people are playing?")
    b = BlackJack(num)
    rounds = input("How many rounds are you playing?")
    b.game(rounds)


main()