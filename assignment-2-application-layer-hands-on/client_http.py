import aiohttp
import asyncio
import logging
from typing import Literal, Callable, Iterable

async def request_and_log_site_info(session: aiohttp.ClientSession, 
                        method: Literal['get', 'post'],
                        url: str
                    ) -> None:
    try:
        logging.info(f"Fetching [{method.upper()}] on {url}")
        async with session.request(method, url) as resp:
            logging.info(f"Status Code: {resp.status}")
            logging.info("Headers:")
            for key, value in resp.headers.items():
                logging.info(f"\t\t{key}: {value}")
            body = await resp.read()
            logging.info(f"Body Preview: {body[:50]}{'...' if len(body) > 50 else ''}") 
    except Exception as e:
        logging.error(f"{method.upper()} Request failed: {e}")
    
async def main(concurrent: bool = False) -> None:
    async with aiohttp.ClientSession() as session:
        if not concurrent:
            await request_and_log_site_info(session, 'get', 'https://example.com')
            logging.info('-'*50)
            await request_and_log_site_info(session, 'post', 'https://example.com')
        else:
            tasks = map(asyncio.create_task, (
                request_and_log_site_info(session, 'get', 'https://example.com'),
                request_and_log_site_info(session, 'post', 'https://example.com')
            ))
            await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(filename='http.log', mode='a')
        ]
    )
    asyncio.run(main())