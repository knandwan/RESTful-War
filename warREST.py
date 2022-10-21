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

# Card, consisting of a value and suit
class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return "{0}, {1}".format(self.value, self.suit)

# Deck of cards
def deck():
    cards = []
    for value in card_values:
        for suit in card_suits:
            if value in face_values_forward:
                cards.append(Card(face_values_forward[value], suit))
            else:
                cards.append(Card(value, suit))
    return cards

# Randomized equal split of playing cards between two players
def split_deck(cards):
    set1 = random.sample(cards, 26)
    # Intermediary list for shuffling
    intset = [i for i in cards if i not in set1]
    # Randomized/shuffled selection from intermediary list
    set2 = random.sample(intset, 26)
    return set1, set2
i = 0
# Game play in accordance with defined rules
def play(set1, set2):
    global i
    i += 1
    winner = -1
    p1_empty = False
    p2_empty = False
    # Drawing cards, play is from first card to last card through pop
    try:
        player1_card = set1.pop(0)
    except:
       p1_empty = True 
       #return [], set2, 2
    try:
        player2_card = set2.pop(0)
    except:
       p2_empty = True
       #return set1, [], 1
    
    if p1_empty and p2_empty:
        return [], [], -1
    elif p1_empty:
        return [], set2, 2
    elif p2_empty:
        return set1, [], 1

    player1_value = player1_card.value if player1_card.value not in face_values_reverse else face_values_reverse[player1_card.value]
    player2_value = player2_card.value if player2_card.value not in face_values_reverse else face_values_reverse[player2_card.value]
    if player1_value > player2_value:
        winner = 1
        set1.append(player1_card); set1.append(player2_card)
    elif player2_value > player1_value:
        winner = 2
        set2.append(player2_card); set2.append(player1_card)
    elif player1_value == player2_value:
        try:
            player1_skip = set1.pop(0)
        except:
            return [] , set2, 2
        try:              
            player2_skip = set2.pop(0)
        except:
            return set1, [], 1

        # Recursive function call
        set1, set2, winner = play(set1, set2)    
        if winner == 1:
            set1.append(player1_card); set1.append(player2_card)
            set1.append(player1_skip); set1.append(player2_skip)
        elif winner == 2:
            set2.append(player2_card); set2.append(player1_card)
            set2.append(player2_skip); set2.append(player1_skip)

    return set1, set2, winner
            
# Database connection
def db_connection():
    conn = sqlite3.connect("playerwins.sqlite")
    return conn

class StartGame(Resource):    
    def get(self):
        # List of playing cards
        cards = deck()

        # Player's playing card set
        player1_set, player2_set = split_deck(cards)

        set1, set2, winner = play(player1_set, player2_set)
        counter = 0
        conn = db_connection()
        cursor = conn.cursor()

        while set1 and set2:
            counter += 1
            set1, set2, winner = play(set1, set2)
        
        if winner == 1:
            cursor = cursor.execute(""" UPDATE playerwins SET wins = wins + 1 WHERE player = "Player1" """)
            conn.commit()
            return {"winner:": "Player 1"}
        elif winner == 2:
            cursor = cursor.execute(""" UPDATE playerwins SET wins = wins + 1 WHERE player = "Player2" """)
            conn.commit()
            return {"winner:": "Player 2"}
        else:
            return {"error:": "Error error error"}


class PlayerWins(Resource):
    def get(self):
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor = conn.execute(""" SELECT * FROM playerwins """)
        return dict(cursor.fetchall())


def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(StartGame, "/startgame")
    api.add_resource(PlayerWins, "/playerwins")
    app.run(debug=True)

if __name__ == "__main__":
    main()