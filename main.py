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
def get_moxfield_lists(proxy, deck_address, pause) -> list:
    ret_list = []
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get(deck_address)
    driver.implicitly_wait(pause)
    decklist_dirty = driver.find_elements(By.CLASS_NAME, "table-deck-row-link.text-body")
    decklist_dirty = [a for a in decklist_dirty if a] # remove blanks
    decklist = set(decklist_dirty) # remove possible duplicates by converting find_elements return list to set.
    for imxrt in decklist:
        ret_list.append(imxrt.text)
    driver.close()

    return ret_list

# Script to get individual lists from tappedout.com
def get_tappedout_lists(proxy, deck_address1, pause) -> list:
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get(deck_address1)
    driver.implicitly_wait(pause)
    decklist_dirty = driver.find_elements(By.CLASS_NAME, "member")
    decklist_dirty = [b for b in decklist_dirty if b] # remove blanks
    decklist_set = set(decklist_dirty) # remove possible duplicates by converting find_elements return list to set.
    ret_list1 = [c.text.split(' ', 1)[1] for c in decklist_set]
    return ret_list1

# create txt log incase the scrape gets interrupted
def log_scrape(loglink, qty):
    f = open("scrape_log.txt", "a")
    f.write("scraped " + str(qty) + " from: " + str(loglink) + "\n")
    f.close()

# Write data to pickle file using pandas.
def backup_work(scrapped_list):
    df1 = pd.read_pickle(r"C:\Users\dmcfa\Desktop\cedh_webscrape1.pk1")
    # df1 = pd.DataFrame(scrapped_list, columns=['Card_names'])
    df2 = pd.DataFrame(scrapped_list, columns=['Card_names'])
    df_to_save = pd.concat([df1, df2], axis=0)
    df_to_save.to_pickle(r"C:\Users\dmcfa\Desktop\cedh_webscrape1.pk1")
    print(df_to_save.tail(4))
    print(str(df_to_save.shape[0]) + ' Rows in Pickle file.')

# Function for scraping the 400 deck lists from the DDB.
def scraper():
    proxies_list = asyncio.run(async_proxy_pooll.main_proxy_pool())
    print('Returned ' + str(len(proxies_list)) + ' proxies.')
    while_loop_cntrl, valid_proxy, mx_deck_address, tp_deck_address = 0, "", "", ""
    moxfld, tppdout = ddb_list()
    to = len(tppdout)
    print("Moxfield decklists: " + str(len(moxfld)) + " TappedOut decklists: " + str(len(tppdout)))

    for x in range(len(moxfld)):
        pause = random.randint(5, 15)
        valid_proxy = proxies_list.pop()
        print('Proxies remaining: ' + str(len(proxies_list)))
        if len(proxies_list) == 0:
            proxies_list = asyncio.run(async_proxy_pooll.main_proxy_pool())
        mx_deck_address = moxfld.pop()
        print('Moxfield Decks left: ' + str(len(moxfld)))
        mx_deck_list = get_moxfield_lists(valid_proxy, mx_deck_address, pause)
        backup_work(mx_deck_list)
        print(mx_deck_address + ' Scraped with proxy address: ' + str(valid_proxy))
        log_scrape(mx_deck_address, len(mx_deck_list))
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
        tp_deck_list = get_tappedout_lists(valid_proxy, tp_deck_address, pause)
        backup_work(tp_deck_list)
        print(tp_deck_address + ' Scraped with proxy address: ' + str(valid_proxy))
        log_scrape(tp_deck_address, len(tp_deck_list))
        while_loop_cntrl += 1
    if len(moxfld) == 0 and len(tppdout) == 0:
        print('Decks scraped: ' + str(while_loop_cntrl))


if __name__ == "__main__":
    scraper()