from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import random



def ddb_list() -> list:
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    moxfield = []
    archideckt = []
    tappedout = []
    link_list = []
    project_href = [i['href'] for i in soup.find_all('a', href=True)]
    for i in project_href:
        mxfld = re.search("moxfield", i)
        arch = re.search("archidekt", i)
        tppd = re.search("tappedout", i)
        if mxfld != None:
            moxfield.append(mxfld.string)
        if arch != None:
            archideckt.append(arch.string)
        if tppd != None:
            tappedout.append(tppd.string)

    for a in moxfield:
        link_list.append(a)
    for b in archideckt:
        link_list.append(b)
    for c in tappedout:
        link_list.append(c)
    """    f = open("list", "w")
    for d in link_list:
        f.write(d + "\n")
    f.close()"""
    return link_list


def get_moxfield_lists():
# Use headless browser to scrape deck list
    pause = random.randint(5, 15)
    options = Options()
    options.add_argument("--headless")
    s = Service('C:\chromedriver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)

    driver.get('https://www.moxfield.com/decks/urs4pKTeCUyZ-FJimN5prA')
    driver.implicitly_wait(pause)

    decklist = driver.find_elements(By.CLASS_NAME, "table-deck-row-link.text-body")

    for i in decklist:
        print(i.text)

    driver.close()

get_moxfield_lists()