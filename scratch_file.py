proxies_list = open(r'C:\Users\dmcfa\PycharmProjects\cEDH Data\newBigProxyList.txt', "r").read().strip().split("\n")
f = open('MasterProxyList', 'a')
for i in proxies_list:
    f.write('http://' + i.strip() + '\n')