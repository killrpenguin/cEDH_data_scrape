from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests
import random
import re

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
def get_moxfield_lists(proxy, deck_address) -> list:
    ret_list = []
    pause = random.randint(5, 15)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--proxy_server=%s" % proxy)
    s = Service('C:\chromedriver\chromedriver.exe')

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(deck_address)
    driver.implicitly_wait(pause)
    decklist = driver.find_elements(By.CLASS_NAME, "table-deck-row-link.text-body")

    for imxrt in decklist:
        ret_list.append(imxrt.text)
    driver.close()

    return ret_list

# Script to get individual lists from tappedout.com
def get_tappedout_lists(proxy, deck_address1) -> list:
    ret_list1 = []
    pause = random.randint(5, 15)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--proxy_server=%s" % proxy)
    s = Service('C:\chromedriver\chromedriver.exe')

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(deck_address1)
    driver.implicitly_wait(pause)
    decklist = driver.find_elements(By.CLASS_NAME, "card-link.card-hover")

    for itpd in decklist:
        ret_list1.append(itpd.text)
    driver.close()
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
    proxies_list = open("tested_proxies", "r").read().strip().split("\n")
    while_loop_cntrl, valid_proxy, mx_deck_address, tp_deck_address = 0, "", "", ""
    VALID_STATUSES = [200, 301, 302, 307, 404]
    moxfld, tppdout = ddb_list()
    print("Moxfield decklists: " + str(len(moxfld)) + " TappedOut decklists: " + str(len(tppdout)))
    while while_loop_cntrl <= 10000:
        # Check the proxy is clean
        for proxy in proxies_list:
            try:
                response = requests.get(url="http://ident.me/", proxies={'http': f"http://{proxy}"}, timeout=10)
                if response.status_code in VALID_STATUSES:
                    valid_proxy = proxy
                    proxies_list.remove(proxy)
                    break
            except Exception as e:
                print("Exception: ", type(e))
        if len(proxies_list) == 0:
            proxies_list = open("tested_proxies", "r").read().strip().split("\n")
        if len(moxfld) > 0:
            for mx_deck_addr in moxfld:
                mx_deck_address = mx_deck_addr
                moxfld.remove(mx_deck_addr)
                print('Moxfield Decks left: ' + str(len(moxfld)))
                break
            mx_deck_list = get_moxfield_lists(valid_proxy, mx_deck_address)
            mx_deck_list = [a for a in mx_deck_list if a]
            backup_work(mx_deck_list)
            print(mx_deck_address)
            log_scrape(mx_deck_address, len(mx_deck_list))
        while_loop_cntrl += 1
        print('Decks scraped: ' + str(while_loop_cntrl))
        if len(tppdout) > 0:
            for tp_deck_addr in tppdout:
                tp_deck_address = tp_deck_addr
                tppdout.remove(tp_deck_addr)
                print('TappedOut Decks left: ' + str(len(tppdout)))
                break
            tp_deck_list = get_tappedout_lists(valid_proxy, tp_deck_address)
            tp_deck_list = [b for b in tp_deck_list if b]
            backup_work(tp_deck_list)
            print(tp_deck_address)
            log_scrape(tp_deck_address, len(tp_deck_list))
        if len(moxfld) == 0 and len(tppdout) == 0:
           break

        while_loop_cntrl += 1
        print('Decks scraped: ' + str(while_loop_cntrl))



scraper()