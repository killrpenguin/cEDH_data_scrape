import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions


list_cleaning = ['Buy', 'Sell', '€', 'View', '$', 'N/A']
proxy = 'http://141.148.63.29:80'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get('https://www.moxfield.com/decks/Q5GFGDOtqk6-ri92lbDxsg')
driver.implicitly_wait(10)
decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='deckview']")
decklist = [a.text.strip().split('\n') for a in decklist_dirty]
decklist = [a for a in decklist[0]]
decklist = [a for a in decklist if 'Buy' not in a if 'Add' not in a
            if 'Sell' not in a if 'N/A' not in a if 'View' not in a
            if 'Expand' not in a if '$' not in a if '€' not in a
            if '(' not in a if '1' not in a if '2' not in a]
for i in decklist:
    print(i)
driver.close()
