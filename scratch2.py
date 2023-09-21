import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dataclasses import dataclass, field


xpath = '//*[@id="proxytable"]/tr'
page = "https://proxyscrape.com/free-proxy-list-f"
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')

proxy_objects = []
@dataclass(kw_only=True)
class Proxies:
    address: str = field(default=str)
    protocol: str = field(default=str)
    latency: str = field(default=str)


with selenium.webdriver.Edge(options=edge_options) as driver:
    wait = WebDriverWait(driver, 30)
    driver.get(page)
    proxy_table = wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
    proxy_table = [proxy.text for proxy in proxy_table]
    for i in proxy_table:
        address = re.search("^\d.+?\s\d.+?\s", i)
        protocol = re.search("H.+?\s|So.+?\d\s", i)
        latency = re.search("\d{2,4}ms", i)
        proxy_detail = Proxies(address=address.group().replace(" ", ":", 1).strip(),
                               protocol=protocol.group().strip(),
                               latency=latency.group().strip()
                               )

    print(len(driver.page_source))