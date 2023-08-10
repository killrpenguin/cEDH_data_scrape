import aiohttp
import asyncio
import logging

async def on_request_start(session, context, params):
    logging.getLogger('aiohttp.client').debug(f'Starting request <{params}>')
    f'Starting request <{params}>'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main_test():
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        html = await fetch(session, 'http://ident.me/')
        print(html)

asyncio.run(main_test())