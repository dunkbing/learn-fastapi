from fastapi import FastAPI, Request
import sentry_sdk
import time
from .database import Base, engine
from .config import settings
from .user import views as user_views
from .item import views as item_views
from .image import views as image_views
from .manga import views as manga_views
from .genre import views as genre_views
from .chapter import views as chapter_views
from .chapter_image import views as chapter_image_views

app = FastAPI()
sentry_sdk.init(dsn=settings.sentry_dsn)
Base.metadata.create_all(bind=engine)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.middleware('http')
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)
            user_id = "database_user_id"  # when available
            scope.user = {
                "ip_address": request.client.host,
                "id": user_id
            }
            sentry_sdk.capture_exception(e)
        raise e

app.include_router(user_views.user_router, prefix='/users', tags=['users'])
app.include_router(item_views.item_router, prefix='/items', tags=['items'])
app.include_router(image_views.image_router, prefix='/images', tags=['images'])
app.include_router(manga_views.manga_router, prefix='/mangas', tags=['mangas'])
app.include_router(genre_views.genre_router, prefix='/genres', tags=['genres'])
app.include_router(chapter_views.chapter_router,
                   prefix='/chapters', tags=['chapters'])
app.include_router(chapter_image_views.chapter_image_router,
                   prefix='/chapter_images', tags=['chapter_images'])


@app.get("/")
async def root():
    return {"message": "Hello World"}
