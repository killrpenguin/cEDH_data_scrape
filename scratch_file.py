import selenium
from selenium import webdriver
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import re


deck_xpath = """/html/body/div[1]/main/div[8]/div[1]/div[2]/div[1]"""
author_xpath = """//html//body//div[1]//main//div[3]//div[2]//div[1]//div//div[1]//div//div[2]//div"""
name_xpath = """//html//body//div[1]//main//div[3]//div[2]//div[1]//div//form//h1//span//span"""
proxy = 'http://45.225.184.177:999'
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get("https://www.moxfield.com/decks/gxBZePi4SkqoDoq3W_EHOg")
errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, timeout=5, poll_frequency=.2, ignored_exceptions=errors)

author = wait.until(ec.presence_of_element_located((By.XPATH, author_xpath))).text.split(',')
author = [name.strip() for name in author]
deck_name = wait.until(ec.presence_of_element_located((By.XPATH, name_xpath))).text
commander_string = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.replace('\n', '')
commander = re.search("(?<=r\(\d\)\d).*?(?=Ba.+\(\d\))", commander_string).group()
deck_list = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.split('\n')
deck_list = [re.sub("^[0-9]|^[0-9][0-9]|^C.+(.)|^A.+(.)|^E.+(.)|^B.+(.)|^P.+(.)|^I.+(.)|^S.+(.)|^L.+(.)", '', card) for card in deck_list]
deck_list = [card.strip() for card in deck_list if '' != card]
print(commander)

driver.close()