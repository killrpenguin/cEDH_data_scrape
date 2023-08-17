import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

proxy = 'http://139.99.237.62:80'
"""f = open("text_decks.txt", "r").read().strip().split("\n")
output = open('test_list.txt', 'x')"""
edge_options = EdgeOptions()
edge_options.use_chromium = True
# edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu'), edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get("https://www.moxfield.com/decks/_mbYBr7Ft0CYPdu1B3I4lA")
driver.implicitly_wait(10)
# view_mode = Select(driver.find_element(By.XPATH, "//select[@id='viewMode']"))
group_by = driver.find_element(By.XPATH, "//select[@id='groupBy']")
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(group_by).click(group_by).perform()
# sort_by = Select(driver.find_element(By.XPATH, "//select[@id='sortBy']"))
# view_mode.select_by_value('condensedTable')
# group_by.select_by_value('none')
# sort_by.select_by_value('name')
decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='deckview']//div[2]//child::div[1]")
# decklist = [a.text.strip().split('\n') for a in decklist_dirty]
for i in decklist_dirty:
    print(i.text)
# decklist = [a for a in decklist[0]]

button = driver.find_element(By.CLASS_NAME, u"infoDismiss")
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(group_by).click(group_by).perform()
