import asyncio
import aiohttp
from typing import List

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return {
            'url': url,
            'status': response.status,
            'content': await response.text()
        }

async def scrape_urls(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    # Example URLs to scrape
    urls = [
        'https://python.org',
        'https://fastapi.tiangolo.com',
        'https://docs.python.org'
    ]
    
    try:
        results = await scrape_urls(urls)
        for result in results:
            print(f"URL: {result['url']}")
            print(f"Status: {result['status']}")
            print(f"Content length: {len(result['content'])} bytes")
            print("-" * 50)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
