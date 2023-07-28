import requests


proxies_list = open("http.txt", "r").read().strip().split("\n")
unchecked_set = set(proxies_list)
working_set, broken_set = set(), set()
VALID_STATUSES = [200, 301, 302, 307, 404]



def reset_proxy(proxy):
    unchecked_set.add(proxy)
    working_set.discard(proxy)
    broken_set.discard(proxy)


def set_working(proxy):
    unchecked_set.discard(proxy)
    working_set.add(proxy)
    broken_set.discard(proxy)


def set_not_working(proxy):
    unchecked_set.discard(proxy)
    working_set.discard(proxy)
    broken_set.add(proxy)

def get(url, proxy):
    try:
        # Send proxy requests to the final URL
        response = requests.get(url, proxies={'http': f"http://{proxy}"}, timeout=10)
        if response.status_code in VALID_STATUSES:
            print(response.status_code, response.text)
            set_working(proxy)
        else:
            set_not_working(proxy)
    except Exception as e:
        print("Exception: ", type(e))
        set_not_working(proxy)
    f = open("tested_proxies", "w")
    for i in working_set:
        f.write(i + "\n")

def check_proxies():
    # proxy_from_list = proxies_list.pop()
    for proxy_from_list in proxies_list:
        get(url="http://ident.me/", proxy=proxy_from_list)


