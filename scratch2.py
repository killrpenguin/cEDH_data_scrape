import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions

proxy = 'http://37.113.130.140:8080'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get('https://tappedout.net/mtg-decks/shuffle-hulk/')
driver.implicitly_wait(5)
decklist_dirty = driver.find_elements(By.CLASS_NAME, "member")
print(len(decklist_dirty))
decklist_dirty = [b for b in decklist_dirty if b]  # remove blanks
decklist_set = set(decklist_dirty)  # remove possible duplicates by converting find_elements return list to set.
decklist = [c.text.split(' ', 1)[1] for c in decklist_set]
