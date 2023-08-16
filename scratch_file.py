import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions

proxy = 'http://139.99.237.62:80'
f = open("text_decks.txt", "r").read().strip().split("\n")
output = open('test_list.txt', 'x')
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)

    driver.get(i)
    driver.implicitly_wait(5)
    decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='deckview']")
    decklist = [a.text.strip().split('\n') for a in decklist_dirty]
    decklist = [a for a in decklist[0]]
    decklist = [a for a in decklist if a.startswith('Buy') is False]
    decklist = [a for a in decklist if a.startswith('Sell') is False]
    decklist = [a for a in decklist if a.startswith('€') is False]
    decklist = [a for a in decklist if a.startswith('View') is False]
    decklist = [a for a in decklist if a.startswith('$') is False]
    decklist = [a for a in decklist if a.startswith('€') is False]
    decklist = [a for a in decklist if a.startswith('N/A') is False]
    decklist = [a for a in decklist if a.endswith('Expand') is False]
    decklist = [a for a in decklist if a.endswith('List') is False]
    decklist = [a for a in decklist if (a != '1') and (a != '2')]

driver.close()
