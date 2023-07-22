from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

# Use headless browser to scrape deck list
options = Options()
options.headless = True
f = open("Heliod.txt", "a")
driver = webdriver.Chrome('C:\chromedriver', options=options)

driver.get('https://www.moxfield.com/decks/urs4pKTeCUyZ-FJimN5prA')
driver.implicitly_wait(10)

decklist = driver.find_elements(By.CLASS_NAME, "table-deck-row-link.text-body")
deckname = driver.find_elements(By.CLASS_NAME, "deck-header-name")
for i in decklist:
    print(i.text)
    f.write(i.text + '\n')


driver.close()

# Gather list from DDB
url = "https://cedh-decklist-database.com/"
page = requests.get(url)
f = open("list.txt", "a")

soup = BeautifulSoup(page.content, "html.parser")

project_href = [i['href'] for i in soup.find_all('a', href=True)]
for i in project_href:
    print(i + "\n")
    f.write(i + "\n")

f.close()