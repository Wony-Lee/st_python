# from bs4 import BeautifulSoup
from dotenv import load_dotenv
import aiohttp
import asyncio
import os
import aiofiles


async def img_downloader(session, img):
    img_name = img.split("/")[-1].split("?")[0]

    try:
        os.mkdir('./images')
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{img_name}", mode="wb") as file:
                img_data = await response.read()
                await file.write(img_data)


async def fetch(session, url):
    ClientId = os.environ.get("X-Naver-Client-Id")
    ClientKey = os.environ.get("X-Naver-Client-Secret")
    headers = {
        "X-Naver-Client-Id": ClientId,
        "X-Naver-Client-Secret": ClientKey
        }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)

        await asyncio.gather(*[img_downloader(session, img) for img in images])


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{BASE_URL}?query={keyword}&display=20&start={1+ i*20}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
