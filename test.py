from warREST import play, Card

card_values_lower = list(range(2,8))
card_values_higher = list(range(9,15))
card_suits = ["spades", "hearts", "diamonds", 'clubs']

def test1():
    cl, ch = list(), list()

 

    for s in card_suits:
        for t in [(s, q) for q in card_values_lower]:
            #print("lo", Card(t[1], t[0]))
            cl.append(Card(t[1], t[0]))
        
        for t in [(s, q) for q in card_values_higher]:
            #print("hi", Card(t[1], t[0]))
            ch.append(Card(t[1], t[0]))
    
    for i in card_suits[:2]:
        cl.append(Card(8, i))

    for j in card_suits[2:]:
        ch.append(Card(8, j))

    # for i in cl:
    #     print("lo", i)

    # for i in ch:
    #     print("hi", i)


    set1, set2, winner = play(cl, ch)

    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    assert(winner == 2)
    

def test2():
    cl, ch = list(), list()
    for s in card_suits[:2]:
        for t in [(s, q) for q in card_values_lower]:
            cl.append(Card(t[1], t[0]))

        for t in [(s, q) for q in card_values_higher]:
            cl.append(Card(t[1], t[0]))

    for s in card_suits[2:]:
        for t in [(s, q) for q in card_values_lower]:
            ch.append(Card(t[1], t[0]))

        for t in [(s, q) for q in card_values_higher]:
            ch.append(Card(t[1], t[0]))

    for i in card_suits[:2]:
        ch.append(Card(8, i))

    for i in card_suits[2:]:
        cl.append(Card(8, i))
    for i in cl:
        print("lo", i)

    for i in ch:
        print("hi", i)
    set1, set2, winner = play(cl, ch)
    while set1 and set2:
        set1, set2, winner =  play(set1, set2)
    
    print(winner)
print("Test1")
test1()
print("Test2")
test2()