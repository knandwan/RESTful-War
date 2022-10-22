import random, sqlite3
from re import I

from flask import Flask
from flask_restful import Api, Resource


# Card Value and Suit generation
card_values = list(range(2,15))
card_suits = ["spades", "hearts", "diamonds", 'clubs']

# Face cards mappings for debugging and ease of printing
face_values_forward = {14:"A", 13:"K", 12:"Q", 11:"J"}
face_values_reverse = {"A":14, "K":13, "Q":12, "J":11}

# Card
## Each card consists of a value and corresponding suit
class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return "{0}, {1}".format(self.value, self.suit)

# Deck of cards
## Generating 52 cards in a deck, as a list of card objects
def deck():
    cards = []
    for value in card_values:
        for suit in card_suits:
            if value in face_values_forward:
                cards.append(Card(face_values_forward[value], suit))
            else:
                cards.append(Card(value, suit))
    return cards

# Deck split
## Randomized equal split of playing cards between two players, each gets 26 cards
def split_deck(cards):
    set1 = random.sample(cards, 26)
    # Intermediary list for shuffling
    intset = [i for i in cards if i not in set1]
    # Randomized/shuffled selection from intermediary list
    set2 = random.sample(intset, 26)
    return set1, set2

# Game play
# A round of game play, each player draws a card and plays round per game rules
def play(set1, set2):
    winner = -1
    player1_blank = False
    player2_blank = False

    # Drawing cards, play is from first card to last card through pop
    try:
        player1_card = set1.pop(0)
    except:
       player1_blank = True 
    try:
        player2_card = set2.pop(0)
    except:
       player2_blank = True
    
    # Validating whether players have exhausted their decks
    if player1_blank and player2_blank:
        # If both players simultaneously exhaust their decks, no winner
        return [], [], -1
    elif player1_blank:
        # Player 1 exhausts his deck, Player 2 is the winner
        return [], set2, 2
    elif player2_blank:
        # Player 2 exhausts his deck, Player 1 is the winner
        return set1, [], 1

    # Reverse mapping face cards from representational value to numeric value
    if player1_card.value in face_values_reverse:
        player1_value = face_values_reverse[player1_card.value]
    else:
        player1_value = player1_card.value
    if player2_card.value in face_values_reverse:
        player2_value = face_values_reverse[player2_card.value]
    else:
        player2_value = player2_card.value
    
    # Game play according to defined game rules
    if player1_value > player2_value:
        winner = 1
        set1.append(player1_card)
        set1.append(player2_card)
    elif player2_value > player1_value:
        winner = 2
        set2.append(player2_card)
        set2.append(player1_card)
    elif player1_value == player2_value:
        # When players are at war, they skip a card in their decks and play another round
        ## Player 1 exhausts his deck, Player 2 is the winner
        try:
            player1_skip = set1.pop(0)
        except:
            return [] , set2, 2
        ## Player 2 exhausts his deck, Player 1 is the winner
        try:              
            player2_skip = set2.pop(0)
        except:
            return set1, [], 1
        ## Players start another round of play, recursive function call
        set1, set2, winner = play(set1, set2)    
        # Winner of a war gets the skipped card and the cards of his opponent 
        if winner == 1:
            set1.append(player1_card)
            set1.append(player2_card)
            set1.append(player1_skip)
            set1.append(player2_skip)
        elif winner == 2:
            set2.append(player2_card)
            set2.append(player1_card)
            set2.append(player2_skip)
            set2.append(player1_skip)

    return set1, set2, winner
            
# Database connection
## Establishing a connection with sqlite db
def db_connection():
    conn = sqlite3.connect("playerwins.sqlite")
    return conn

# StartGame Endpoint
## Inheriting resource building block and overriding HTTP GET method to start war game between two players
class StartGame(Resource):    
    def get(self):
        # Connection establishment with db, cursor initialization for query execution
        conn = db_connection()
        cursor = conn.cursor()

        # List of playing cards
        cards = deck()

        # Player's playing card set
        player1_set, player2_set = split_deck(cards)

        # First round of game play
        set1, set2, winner = play(player1_set, player2_set)

        # Gameplay in this game continues till a winner is decided, through exhaustion of decks
        while set1 and set2:
            set1, set2, winner = play(set1, set2)
        
        # Each player's win is persisted in db to keep track of lifetime wins
        if winner == 1:
            cursor = cursor.execute(""" UPDATE playerwins SET wins = wins + 1 WHERE player = "Player1" """)
            conn.commit()
            return {"winner:": "Player 1"}
        elif winner == 2:
            cursor = cursor.execute(""" UPDATE playerwins SET wins = wins + 1 WHERE player = "Player2" """)
            conn.commit()
            return {"winner:": "Player 2"}
        elif winner == -1:
            return {"winner:": "No winner, game has been drawn"}
        else:
            return {"error:": "Error error error"}

# Playerwins Endpoint
## Inheriting resource building block and overriding HTTP GET method to query sqlite db and return player career wins
class PlayerWins(Resource):
    def get(self):
        conn = db_connection()
        cursor = conn.cursor()
        
        # Query db and return each player career wins
        cursor = conn.execute(""" SELECT * FROM playerwins """)
        return dict(cursor.fetchall())

# Main function
## Handles flask application creation, endpoint registration
def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(StartGame, "/startgame")
    api.add_resource(PlayerWins, "/playerwins")
    app.run(debug=True)

if __name__ == "__main__":
    main()