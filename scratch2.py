import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions

decklist_reg = []
proxy = 'http://141.148.63.29:80'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get('https://www.moxfield.com/decks/Q5GFGDOtqk6-ri92lbDxsg')
driver.implicitly_wait(10)
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
print(deck_name.text.strip())
decklist = [print(i) for i in decklist]
driver.close()
