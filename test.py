from warREST import play, Card

card_values_lower = list(range(2,8))
card_values_higher = list(range(9,15))
card_suits = ["spades", "hearts", "diamonds", 'clubs']

def test1():
    cl, ch = list(), list()
    for s in card_suits:
        for t in [(s, q) for q in card_values_lower]:
            cl.append(Card(t[0], t[1]))
        
        for t in [(s, q) for q in card_values_higher]:
            ch.append(Card(t[0], t[1]))

    
    for i in card_suits[:2]:
        cl.append(Card(i, 8))

    for i in card_suits[2:]:
        ch.append(Card(i, 8))

    for i in cl:
        print("lo", i)

    for i in ch:
        print("hi", i)


    set1, set2, winner = play(cl, ch)
    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    
    print(set1, set2, winner)
    

def test2():
    cl, ch = list(), list()
    for s in card_suits[:2]:
        for t in [(s, q) for q in card_values_lower]:
            cl.append(Card(t[0], t[1]))

        for t in [(s, q) for q in card_values_higher]:
            cl.append(Card(t[0], t[1]))

    for s in card_suits[2:]:
        for t in [(s, q) for q in card_values_lower]:
            ch.append(Card(t[0], t[1]))

        for t in [(s, q) for q in card_values_higher]:
            ch.append(Card(t[0], t[1]))

    for i in card_suits[:2]:
        cl.append(Card(i, 8))

    for i in card_suits[2:]:
        ch.append(Card(i, 8))

    set1, set2, winner = play(cl, ch)
    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    
    print(set1, set2, winner)

test1()
test2()