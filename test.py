import requests
from warREST import play, Card

BASE = "http://127.0.0.1:5000"

card_values_lower = list(range(2,8))
card_values_higher = list(range(9,15))
card_suits = ["spades", "hearts", "diamonds", 'clubs']

# Test 1: Code functionality and logic test
## Hardcoding deck1 with lower value cards and deck2 with higher value cards and testing play functionality
def testPlayer2Winner():
    lowerset, higherset = list(), list()

    # Hardcoding suit of 26 cards, with lower set always having lower value than higher set
    ## Equally splitting 8 value cards with (spades, hearts) suit to lower set and (diamonds, clubs) suit to higher set
    for suit in card_suits[:2]:
        lowerset.append(Card(8, suit))

    for suit in card_suits[2:]:
        higherset.append(Card(8, suit))

    ## Populating lower and higher decks with list of card objects from 2-7 and 7-14 values respectively
    for suit in card_suits:
        for obj in [(suit, value) for value in card_values_lower]:
            lowerset.append(Card(obj[1], obj[0]))
        
        for obj in [(suit, value) for value in card_values_higher]:
            higherset.append(Card(obj[1], obj[0]))

    # Printing lower card deck
    print("\nLower set deck: ")
    for card in lowerset:
        print("(", card, ")", end=" ")
    
    # Printing higher card deck
    print("\nHigher set deck: ")
    for card in higherset:
        print("(", card, ")", end=" ")

    # Single round of play to test war
    set1, set2, winner = play(lowerset, higherset)
    print("\nWinner after first round of play, Player", winner)

    # Deck exhaustion and game winner logic test
    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    print("Winner of the game, Player", winner)

    try:
        assert(winner==2)
    except:
        print("Testcase failed")

# Test 2: Code functionality and logic test
## Hardcoding deck1 with higher value cards and deck2 with lower value cards and testing play functionality
def testPlayer1Winner():
    lowerset, higherset = list(), list()

    # Hardcoding suit of 26 cards, with lower set always having lower value than higher set
    ## Equally splitting 8 value cards with (spades, hearts) suit to lower set and (diamonds, clubs) suit to higher set
    for suit in card_suits[:2]:
        higherset.append(Card(8, suit))

    for suit in card_suits[2:]:
        lowerset.append(Card(8, suit))

    ## Populating lower and higher decks with list of card objects from 2-7 and 7-14 values respectively
    for suit in card_suits:
        for obj in [(suit, value) for value in card_values_lower]:
            higherset.append(Card(obj[1], obj[0]))
        
        for obj in [(suit, value) for value in card_values_higher]:
            lowerset.append(Card(obj[1], obj[0]))

    # Printing lower card deck
    print("\nLower set deck: ")
    for card in lowerset:
        print("(", card, ")", end=" ")
    
    # Printing higher card deck
    print("\nHigher set deck: ")
    for card in higherset:
        print("(", card, ")", end=" ")

    # Single round of play to test war
    set1, set2, winner = play(lowerset, higherset)
    print("\nWinner after first round of play, Player", winner)

    # Deck exhaustion and game winner logic test
    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    print("Winner of the game, Player", winner)

    try:
        assert(winner==1)
    except:
        print("Testcase failed")

# Test 3: Edge case logic test
## Hardcoding deck1 and deck2 with the exact same set of cards, same values in same order
def testAlwaysWar():
    player1set, player2set = list(), list()

    # Hardcoding suit of 26 cards, with both player having the same value decks
    ## Equally splitting 8 value cards with (spades, hearts) suit to player1 and (diamonds, clubs) suit to player2
    for suit in card_suits[:2]:
        player1set.append(Card(8, suit))

    for suit in card_suits[2:]:
        player2set.append(Card(8, suit))

    ## Populating player1set with all values from 2-7 and 7-14 for (spades, hearts) suit
    for suit in card_suits[:2]:
        for obj in [(suit, value) for value in card_values_lower]:
            player1set.append(Card(obj[1], obj[0]))

        for obj in [(suit, value) for value in card_values_higher]:
            player1set.append(Card(obj[1], obj[0]))

    ## Populating player2set with all values from 2-7 and 7-14 for (diamonds, clubs) suit
    for s in card_suits[2:]:
        for obj in [(suit, value) for value in card_values_lower]:
            player2set.append(Card(obj[1], obj[0]))

        for obj in [(suit, value) for value in card_values_higher]:
            player2set.append(Card(obj[1], obj[0]))

    # Printing player1 card deck
    print("\nLower set deck: ")
    for card in player1set:
        print("(", card, ")", end=" ")
    
    # Printing player2 card deck
    print("\nHigher set deck: ")
    for card in player2set:
        print("(", card, ")", end=" ")

    # Single round of play to test war
    set1, set2, winner = play(player1set, player2set)
    if winner == -1:
        print("\nDrawn Game, both players ran out of their decks simultaneously")
    else: 
        print("\nWinner after first round of play, Player", winner)

    # Deck exhaustion and game winner logic test
    ## The game must terminate on a single round of play, as both players have the same values in same order
    while set1 and set2:
        print("Execution should never enter this loop")
        set1, set2, winner =  play(set1, set2)
    
    try:
        assert(winner==-1)
    except:
        print("Testcase failed")

# Test 4: REST endpoints functionality test
## Testing initial and updated states of the database by running the /playerwins and /startgame endpoints
def testEndpoints():
    # Initial database state
    ## If the initial win counts is not zero, the testcase fails
    print("\nTesting playerwins endpoint")
    initialGameFlag = False
    initialstate = requests.get(BASE + "/playerwins")
    print("Initial player win counts per db", initialstate.json())

    for playerWin in initialstate.json().values():
        if playerWin == 0:
            initialGameFlag = True
        else:
            initialGameFlag = False

    try:
        assert initialGameFlag
    except:
        print("Testcase failed")

    # Validating database state after 5 random game instances
    ## If the count of game wins does not match the count stored on the database, the testcase fails
    print("\nTesting startgame and playerwins endpoint concurrently")
    fiveGameFlag = False
    player1wins, player2wins = 0, 0
    for count in range(1,6):
        result = requests.get(BASE + "/startgame")
        print("Winner of round", count, result.json())
        for player in result.json().values():
            if player == 'Player 1':
                player1wins += 1
            elif player == "Player 2":
                player2wins += 1
    
    gamestate = requests.get(BASE + "/playerwins")
    print("Updated player win counts per db", gamestate.json())
    gamewins = []
    for playerWin in gamestate.json().values():
        gamewins.append(playerWin)
    # print(player1wins, player2wins, gamewins)
    if player1wins != gamewins[0] or player2wins != gamewins[1]:
        fiveGameFlag = False
    else:
        fiveGameFlag = True
    
    try:
        assert fiveGameFlag
    except:
        print("Testcase failed")

if __name__ == "__main__":
    # Test 1
    print("Test Case 1: Code functionality and logic test")
    testPlayer2Winner()

    # Test 2
    print("\nTest Case 2: Code functionality and logic test")
    testPlayer1Winner()

    # Test 3
    print("\nTest Case 3: Edge case logic test")
    testAlwaysWar()
    
    # Test 4
    print("\nTest Case 4: REST endpoints functionality test")
    testEndpoints()
