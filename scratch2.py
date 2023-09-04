import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.keys import Keys


view_text = "/html/body/div[5]/div/div/form/div[2]/div[2]/label[1]/div/input"
proxy = "http://103.77.60.14:80"
address = 'https://www.moxfield.com/decks/HYT9YcG0bEK1UMvmEEXtTA'
pause = 5
edge_options = EdgeOptions()
edge_options.use_chromium = True
# edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get(address)
driver.implicitly_wait(pause)
button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[8]/div[1]/div[2]/form/a[1]")
button.click()
"""radio1 = driver.find_element(By.XPATH, view_text)
radio1.click()"""