import selenium
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions

testlink = "https://tappedout.net/mtg-decks/jhoira-stax-storm-cedh-1/?cb=1564924574"
proxy = 'http://141.148.63.29:80'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get(testlink)
driver.implicitly_wait(10)
deck_name = driver.find_element(By.XPATH, "//body[@id='sitebody']"
                                          "//div[@id='main-content']"
                                          "//div[@id='body']"
                                          "//div[@class='container-fluid']"
                                          "//div[@class='row']"
                                          "//div[@class='col-lg-9 col-md-8']"
                                          "//div[@class='row'][1]//div[@class='col-xs-12']"
                                          "//div[@class='well well-jumbotron']/h2")
decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='row board-container'][1]//descendant::div")
decklist = [a.text.strip().split('\n') for a in decklist_dirty]
decklist = [a for b in decklist for a in b]
decklist = [re.sub("^[0-9]x|[1-9][0-9]x", '', a) for a in decklist]
decklist = [a.strip() for a in decklist if a if '(' not in a]
d = {'Deck_Name': deck_name.text.strip(), 'Card_Name': decklist, 'Deck_Link': testlink}

def make_pickle():
    testlst = ['a', 'b']
    dkname = 'TestDeck!'
    a = 'http://www.mx.com/1311'
    testd = {'Card_Name': testlst, 'Deck_Name': dkname, 'Deck_Link': a}
    df = pd.DataFrame(data=testd)
    df1 = df.to_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
    return df1


def backup_work(*, scraped_dict, deck_link):
    make_pickle()
    scraped_dict.update({"Deck_Link": deck_link})
    current_df = pd.read_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
    df2 = pd.DataFrame(data=scraped_dict)
    df_to_save = pd.concat([current_df, df2], ignore_index=True, axis=0)
    df_to_save.to_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
    print(df_to_save['Deck_Name'].head(3))
    print(df_to_save.tail(3))
    print(str(df_to_save.shape[0]) + ' Rows in Pickle file.')

backup_work(scraped_dict=d, deck_link=testlink)
