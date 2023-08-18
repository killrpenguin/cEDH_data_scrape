import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions


proxy = 'http://141.148.63.29:80'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get('https://tappedout.net/mtg-decks/jhoira-stax-storm-cedh-1/?cb=1564924574')
driver.implicitly_wait(10)
decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='row board-container'][1]")
decklist = [a.text.strip().split('1x') for a in decklist_dirty]
decklist = [a.strip().split("\n") for a in decklist[0] if '(' not in a]
decklist = [a[0] for a in decklist]

for a in decklist:
    print(a)

print(len)