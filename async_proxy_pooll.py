import asyncio
import aiohttp

working_set, broken_set = set(), set()
VALID_STATUSES = [200, 301, 302, 307, 404]


def set_working(proxy):
    working_set.add(proxy)
    broken_set.discard(proxy)


def set_not_working(proxy):
    working_set.discard(proxy)
    broken_set.add(proxy)

async def task_coroutine(session, proxy):
    try:
        async with session.get("http://ident.me/", proxy=proxy, timeout=300) as resp:
            if resp.status in VALID_STATUSES:
                print(resp.status)
                set_working(proxy)
            await resp.text()
    except Exception as e:
        print("Exception: ", e)


# custom coroutine
async def main():
    print('main coroutine started')
    proxies_list = open("BigProxyList", "r").read().strip().split("\n")
    tcp_connection = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=tcp_connection) as session:
        try:
            tasks = [asyncio.create_task(task_coroutine(session, i)) for i in proxies_list]
            # wait for each task to complete
            for task in tasks:
                await task
            print('main coroutine done')
            print(len(working_set))
        except Exception as e2:
            print(e2)


asyncio.run(main())



