import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions

clean_list = []
proxy = 'http://141.148.63.29:80'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get('https://tappedout.net/mtg-decks/jhoira-stax-storm-cedh-1/?cb=1564924574')
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

print(deck_name.text.strip())
decklist = [print(i) for i in decklist]