from bs4 import BeautifulSoup
from dotenv import load_dotenv
import aiohttp
import asyncio
import os


async def fetch(session, url):
    ClientId = os.environ.get("X-Naver-Client-Id")
    ClientKey = os.environ.get("X-Naver-Client-Secret")
    headers = {"X-Naver-Client-Id": ClientId, "X-Naver-Client-Secret": ClientKey}
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{BASE_URL}?query={keyword}&display=20&start={i}" for i in range(1, 10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
