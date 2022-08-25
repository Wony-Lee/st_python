from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraiping import NaverBookScraper



BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = BookModel(
    #     keyword="파이썬",
    #     publisher="BJPublic",
    #     price=1200,
    #     image="me.png"
    #     )
    # await mongodb.engine.save(book)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "콜렉터 북북이"
    })


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    # 1. 쿼리에서 검색어 추출
    keyword = q
    # (예외처리)
    # - 검색어가 없다면 사용자에게 검색을 요구 return
    if not keyword:
        context = {"request": request, "title": "콜렉터 북북이"}
        return templates.TemplateResponse(
            "./index.html",
            context
        )
    # - 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다. return
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집한다.
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(
            BookModel,
            BookModel.keyword == keyword
            )
        return templates.TemplateResponse(
            "./index.html",
            {
                "request": request,
                "title": "콜렉터 북북이",
                "keyword": q,
                "books": books
            }
        )

    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        # print(book)
        book_model = BookModel(
            keyword=keyword,
            publisher=book['publisher'],
            price=book['discount'],
            image=book['image']
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    print('Save Success')
    
    # 3. DB에 수집된 데이터를 저장한다.
    # - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    # - 각 모델 인스턴스를 DB에 저장한다.

    return templates.TemplateResponse(
        "./index.html",
        {
            "request": request,
            "title": "콜렉터 북북이",
            "keyword": q,
            "books": books
        }
    )


# 앱이 처음 시작 될 때 on_app_start가 실행될 것읻.
@app.on_event("startup")
async def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    # 앱이 셧다운 될 때 실행될 것.
    mongodb.close
