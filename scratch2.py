import pandas as pd
testdeck = ['a']
test_name = 'TestDeck!'
testlink = 'http://www.somedeck.com/131231231'
d = {'Card_Name': testdeck, 'Deck_Name': test_name, 'Deck_Link': testlink}
df = pd.DataFrame(data=d)
df.to_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
print(df.head())