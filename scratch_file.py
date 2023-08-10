import asyncio
import aiohttp


async def task_coroutine(session, proxy):
    try:
        async with session.get("http://ident.me/", proxy=proxy, timeout=300) as resp:
            print(resp.status)
            await resp.text()
    except Exception as e:
        print("Exception: ", e)


# custom coroutine
async def main_proxy_pool() -> set:
    print('main coroutine started')
    proxies_list = open("BigProxyList", "r").read().strip().split("\n")
    tcp_connection = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=tcp_connection) as session:
        try:
            tasks = [asyncio.create_task(task_coroutine(session, i)) for i in proxies_list]
            for task in tasks:
                await task
        except Exception as e:
            print(e)


asyncio.run(main_proxy_pool())
