import async_proxy_pooll
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from bs4 import BeautifulSoup
import pandas as pd
import selenium
import requests
import random
import re
import asyncio

# Get list of deck links from DDB
def ddb_list() -> tuple:
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    moxfield, tappedout = [], []
    project_href = [spi['href'] for spi in soup.find_all('a', href=True)]
    for phref in project_href:
        mxfld = re.search("moxfield", phref)
        tppd = re.search("tappedout", phref)
        if mxfld != None:
            moxfield.append(mxfld.string)
        if tppd != None:
            tappedout.append(tppd.string)

    return moxfield, tappedout

# Script to get individual lists from moxfield.com
def get_moxfield_lists(*, proxy, deck_address, pause) -> dict:
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get(deck_address)
    driver.implicitly_wait(pause)
    deck_name = driver.find_element(By.XPATH, "//div[@class='deckheader']"
                                              "//div[@class='deckheader-content']/"
                                              "/div[@class='container py-5 text-white']"
                                              "//form/h1[@class='mb-2']/"
                                              "/span[@id='menu-deckname']"
                                              "//span[@class='deckheader-name']")
    decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='deckview']")
    decklist = [a.text.strip().split('\n') for a in decklist_dirty]
    decklist = [a for a in decklist[0]]
    decklist = [re.sub("^\d*x|[A-Za-z]/[A-Za-z]|^\$.+|^€.+|.+\(\d+.*|"
                       "[0-9]|^R.+\sH.+|^[A-Za-z].+@.[A-Za-z].+|"
                       "^V.+\sO.+|^A..\sT.+", '', a) for a in decklist]
    decklist = [a.strip() for a in decklist if '' != a]
    driver.close()
    ret_dict = {'Card_Name': decklist, 'Deck_Name': deck_name}
    return ret_dict

# Script to get individual lists from tappedout.com
def get_tappedout_lists(*, proxy, deck_address1, pause) -> dict:
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get(deck_address1)
    driver.implicitly_wait(pause)
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
    driver.close()
    ret_dict = {'Card_Name': decklist, 'Deck_Name': deck_name}
    return ret_dict

# create txt log incase the scrape gets interrupted
def log_scrape(*, file_to_mod, deck_link, deck_qty):
    file_to_mod.write("scraped " + str(deck_qty) + " from: " + str(deck_link) + "\n")

# Write data to pickle file using pandas.
def backup_work(*, scraped_dict, deck_link, current_df):
    scraped_dict.update({"Deck_Link": deck_link})
    df2 = pd.DataFrame(data=scraped_dict)
    df_to_save = pd.concat([current_df, df2], axis=0)
    df_to_save.to_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
    print(df2.head(1))
    print(df2.tail(3))
    print(str(df_to_save.shape[0]) + ' Rows in Pickle file.')

# Function for scraping the 400 deck lists from the DDB.
def scraper():
    df1 = pd.read_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
    f = open("third scrape/scrape_log.txt", "a")
    proxies_list = asyncio.run(async_proxy_pooll.main_proxy_pool())
    print('Returned ' + str(len(proxies_list)) + ' proxies.')
    while_loop_cntrl, valid_proxy, mx_deck_address, tp_deck_address = 0, "", "", ""
    moxfld, tppdout = ddb_list()
    print("Moxfield decklists: " + str(len(moxfld)) + " TappedOut decklists: " + str(len(tppdout)))

    for x in range(len(moxfld)):
        pause = random.randint(5, 15)
        valid_proxy = proxies_list.pop()
        print('Proxies remaining: ' + str(len(proxies_list)))
        if len(proxies_list) == 0:
            proxies_list = asyncio.run(async_proxy_pooll.main_proxy_pool())
        mx_deck_address = moxfld.pop()
        print('Moxfield Decks left: ' + str(len(moxfld)))
        mx_deck = get_moxfield_lists(proxy=valid_proxy, deck_address=mx_deck_address, pause=pause)
        backup_work(scraped_dict=mx_deck, deck_link=x, current_df=df1)
        print(mx_deck_address + ' Scraped.')
        print('With proxy address: ' + str(valid_proxy))
        log_scrape(file_to_mod=f, deck_link=mx_deck_address, deck_qty=len(mx_deck))
        while_loop_cntrl += 1
        print('Decks scraped: ' + str(while_loop_cntrl))

    for y in range(len(tppdout)):
        pause = random.randint(5, 15)
        valid_proxy = proxies_list.pop()
        print('Proxies remaining: ' + str(len(proxies_list)))
        if len(proxies_list) == 0:
            proxies_list = asyncio.run(async_proxy_pooll.main_proxy_pool())
        print('TappedOut Decks left: ' + str(len(tppdout)))
        tp_deck_address = tppdout.pop()
        tp_deck = get_tappedout_lists(proxy=valid_proxy, deck_address1=tp_deck_address, pause=pause)
        backup_work(scraped_dict=tp_deck, deck_link=y, current_df=df1)
        print(tp_deck_address + ' Scraped.')
        print('With proxy address: ' + str(valid_proxy))
        log_scrape(file_to_mod=f, deck_link=mx_deck_address, deck_qty=len(tp_deck))
        while_loop_cntrl += 1



if __name__ == "__main__":
    scraper()