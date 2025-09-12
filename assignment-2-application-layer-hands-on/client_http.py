import aiohttp
import asyncio
import logging
from typing import Literal

async def request_and_log_site_info(session: aiohttp.ClientSession, 
                        method: Literal['get', 'post'],
                        url: str
                    ) -> list[tuple[int, str]]:
    logs: list[tuple[int, str]] = []
    try:
        logs.append((logging.INFO, f"Fetching [{method.upper()}] on {url}"))
        async with session.request(method, url) as resp:
            logs.append((logging.INFO, f"Status Code: {resp.status}"))
            logs.append((logging.INFO, "Headers:"))
            for key, value in resp.headers.items():
                logs.append((logging.INFO, f"\t\t{key}: {value}"))
            body = await resp.read()
            logs.append((logging.INFO, f"Body Preview: {body[:50]}{'...' if len(body) > 50 else ''}"))
    except Exception as e:
        logs.append((logging.ERROR, f"{method.upper()} Request failed: {e}"))
    return logs
    
async def main(concurrent: bool = False) -> None:
    async with aiohttp.ClientSession() as session:
        if not concurrent:
            logs = await request_and_log_site_info(session, 'get', 'https://example.com')
            for level, msg in logs: logging.log(level, msg)
            logging.info('-'*50)
            logs = await request_and_log_site_info(session, 'post', 'https://example.com')
            for level, msg in logs: logging.log(level, msg)
            logging.info('-'*50)
        else:
            tasks = map(asyncio.create_task, (
                request_and_log_site_info(session, 'get', 'https://example.com'),
                request_and_log_site_info(session, 'post', 'https://example.com')
            ))
            results = await asyncio.gather(*tasks)
            for logs in results:
                for level, msg in logs: logging.log(level, msg)
                logging.info('-'*50)
    
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
