import pandas as pd
testdeck = ['a', 'b', 'c']
test_name = 'TestDeck!'
testlink = 'http://www.somedeck.com/131231231'
d = {'Card_Name': testdeck, 'Deck_Name': test_name, 'Deck_Link': testlink}

print(d['Deck_Name'])