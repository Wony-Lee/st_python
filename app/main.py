from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(
        keyword="파이썬",
        publisher="BJPublic",
        price=1200,
        image="me.png"
        )
    await mongodb.engine.save(book)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "콜렉터 북북이"
    })


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    return templates.TemplateResponse(
        "./index.html",
        {
            "request": request, "keyword": q
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
