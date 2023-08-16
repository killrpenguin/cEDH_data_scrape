import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions


def thx_speedX() -> list:
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get('https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt')
    driver.implicitly_wait(5)
    ret_list = driver.find_elements(By.CLASS_NAME, "react-code-lines.react-code-line-contents.virtual")
    print(len(ret_list))
    for i in ret_list:
        print(i.text)
    return ret_list


thx_speedX()