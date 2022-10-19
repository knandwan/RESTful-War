import random, sys

# Card Value and Suit generation
card_values = list(range(2,15))
card_suits = ["spades", "hearts", "diamonds", 'clubs']

# Face cards mappings for debugging and ease of printing
face_values_forward = {14:"A", 13:"K", 12:"Q", 11:"J"}
face_values_reverse = {"A":14, "K":13, "Q":12, "J":11}

# Card, consisting of a value and suit
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

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

# List of playing cards
cards = deck()
# for card in cards:
#     print(card.suit, card.value)

# Randomized equal split of playing cards between two players
def split_deck():
    set1 = random.sample(cards, 26)
    # Intermediary list for shuffling
    intset = [i for i in cards if i not in set1]
    # Randomized/shuffled selection from intermediary list
    set2 = random.sample(intset, 26)
    return set1, set2

# Player's playing card set
player1_set, player2_set = split_deck()
# if(set(player1_set) & set(player2_set)):
#     print("Common")
# else:
#     print("Not common")

# Game play in accordance with defined rules
def play(set1=player1_set, set2=player2_set):
    winner = -1
    player1_skip = []
    player2_skip = []
    # Drawing cards, play is from last card to first card through pop
    try:
            player1_card = set1.pop(0)
    except IndexError:
            sys.exit("Player 1 Loses! Player 2 Wins")
    try:
            player2_card = set2.pop(0)
    except IndexError:
            sys.exit("Player 1 Wins! Player 2 Loses")
    
    player1_value = player1_card.value if player1_card.value not in face_values_reverse else face_values_reverse[player1_card.value]
    player2_value = player2_card.value if player2_card.value not in face_values_reverse else face_values_reverse[player2_card.value]
    #print(f"Player1: {player1_card.suit} {player1_card.value}")
    #print(f"Player2: {player2_card.suit} {player2_card.value}")
    
    if player1_value > player2_value:
        #print('Adding to player1')
        set1.append(player1_card)
        set1.append(player2_card)
        winner = 1
    elif player2_value > player1_value:
        #print("Adding to player2")
        set2.append(player2_card)
        set2.append(player1_card)
        winner = 2
    elif player1_value == player2_value:
        #print("Equal value")
        player1_skip.append(player1_card) 
        try:
            player1_skip.append(set1.pop(0))
        except IndexError:
            sys.exit("Player 1 Loses! Player 2 Wins")
        #print('Len set1, skip', len(set1), len(player1_skip))        

        player2_skip.append(player2_card) 
        try:
            player2_skip.append(set2.pop(0))
        except IndexError:
            sys.exit("Player 1 Wins! Player 2 Loses")
        #print('Len set2, skip', len(set2), len(player2_skip))      
        
        # Recursive function call
        set1, set2, winner = play(set1, set2)
        if winner == 1:
            for card in player1_skip:
                set1.append(card)
            for card in player2_skip:
                set1.append(card)
        elif winner == 2:
            for card in player1_skip:
                set2.append(card)
            for card in player2_skip:
                set2.append(card)
        elif winner == -1:
            print("weird")

    # l1 = []
    # for card1 in set1:
    #     l1.append(card1.value)
    #print(' '.join(map(str, l1))) 
    # l1 = []
    # for card2 in set2:
    #     l1.append(card2.value)
    #print(' '.join(map(str, l1)))
    return set1, set2, winner

if __name__ == "__main__":
    set1, set2, winner = play()
    counter = 0
    while set1 and set2:
    #while counter<1:
        counter += 1
        set1, set2, winner = play(set1, set2)
        #print(counter)
        #print("winner = ", winner)
        #print(len(set1), len(set2))
        if len(set1) == 0:
            print("Player 1 Loses! Player 2 Wins")
            break
        if len(set2) == 0:
            print("Player 1 Wins! Player 2 Loses")
            break