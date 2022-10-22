# RESTful-War
## War: A RESTful service
War, a simple card game is typically played by two players using a standard deck of cards. The corresponding service in this project has been developed to emulate the war game between two players, Player 1 and Player 2 and persist career wins for each player in a database. The project has been developed in Python, using Flask and sqlite3 packages for REST API and database respectively.

### Gameplay 
The objective of the game is to win all the cards, 52 cards from a normal playing cards deck standpoint. Following are the rules followed for designing the game for this project.
- The deck is divided evenly among the players, giving each their stack of randomized 26 cards. 
- For each round of the game, each player reveals the top card of their deck(this is a "battle") and the player with the higher card takes both of the cards played and moves them to their stack. Aces are high, and suits are ignored.
- If the cards are the same rank, it is War. Each player turns up one card face down and one card face up. The player with the higher cards takes both piles (six cards). If the turned-up cards are again the same rank, each player places another card face down and turns another card face up. The player with the higher card takes all 10 cards, and so on.

### API endpoints
The deployed game service supports two API endpoints, `/startgame` and `/playerwins`
- /startgame endpoint starts the card game between two players, Player 1 and Player 2 and returns the winner of the game and persists the winner in a database
- /playerwins endpoint queries the persisted database to showcase the career wins for each player, Player 1 and Player 2
<p align="center"> <img src="https://github.com/knandwan/RESTful-War/blob/main/apiCurls.jpg" width="1000" class="center"> </p>
<p align="center"> cURL endpoints querying` </p>

## Design
### Service
`warREST.py` file corresponds to the service, and has been designed as modular deployment with initial card deck generation, splitting deck between players and each round of play implemented as seperated functions to allow for ease of both scaling to different usecases and for ease of testing each component individually. The two API endpoints, `/startgame` and `/playerwins` have been further implemented as classes inheriting and building on the flask resources thereby providing easy access to underlying HTTP methods. The API endpoints have been designed to support HTTP GET, as both the endpoints are associated with requesting representation of specified resources and do not correspond to sending any data to the service
### Test
`test.py` file corresponds to the test cases designed to test the service. There are four testcases in total, with the following descriptions describing each of the tests
- Test 1: Code functionality and logic test - this test has been designed to check the logic of the service, and works by hardcoding the two player decks with the second player getting a deck with cards corresponding to all the higher values and the first player getting the deck with all the smaller values. Furthermore the testcase tests the service from both the standpoint of same rank in the first round of play and from higher and lower rank consecutively
- Test 2: Code functionality and logic test - this test can be considered as an inverse of the first case, and works by hardcoding the two player decks with the first player now getting a deck with cards corresponding to the higher values and the second player getting the deck with all the smaller values.
- Test 3: Edge case logic test - this test is a hypothetical case, which ideally in a real-world game should never happen but was designed to ensure correctness of logic should it ever happen. The test case has been designed to provide both the players with the same value decks, with the cards of the same value in respective decks in the same order. Basically both the players have the same value and order of cards, and the game will always be at war with no player actually winning the game
- Test 4: REST endpoints functionality test - this test validates the correctness of endpoint /stargame and /playerwins responses. The first half of the test validates initial database state, wherein playerwins for each of the players should be initialized to 0 and the second half tests the database state after 5 runs of the game. This test is sort of naive and limited in design, in the sense that this test passes only when there is no state saved initially and this is the first instance of the service being started

## Running the Service and Tests
- All the required dependencies for this project have been included as part of the `requirements.txt` file and the same can be executed on host machine where the service is to be deployed as `pip install -r requirements.txt`, with the premise that the host has both python3 and pip configured
- After the dependencies have been installed, the database has to be initialized. The corresponding file `db.py` has been provided for initializing the sqlite3 database and can be executed on the same host machine as `python3 db.py`. A database `playerwins.sqlite` must be successfully created after execution of the same
- The service, `warREST.py` can now be executed on the host as `python3 warREST.py` which inturn exposes the two endpoints `/startgame` and `/playerwins`. The debug mode has been configured to be True which if or when deploying the service to production should be set to False as the same allows executing arbitrary Python code from browser which can be maliciously used by an attacker
- The test suite, `test.py` can further be executed on the host as `python3 test.py` and each of the test cases with there corresponding test decks and values are shown. The tests have assertion statements and if there is any state or functionality failure, then the corresponding testcase prints testfailed message
- The exposed service can further be queried through curl as `curl http://127.0.0.1:5000/startgame` and `curl http://127.0.0.1:5000/playerwins` to test the functionality of the endpoints

## Tradeoffs/Future Improvements
- The current service is limited from the standpoint that the the service only exposes starting game endpoint and the end user has no interaction with the service. A potential improvement could be to make it interactive, from the standpoint that a user plays against a dealer(computer) and the service exposes endpoints to allow user to play the round and then the game continues.
- As a follow up to the first point, providing a UI to allow for user to interact with the service and deploying the same through a cloud provider will allow for ease of scaling user requests, availaibility of the service and application management
- From a security standpoint, securing python APIs and enabling authorization mechanisms can be a possible implementation to make the service more secure. Reference documentation https://auth0.com/docs/quickstart/backend/python/interactive
