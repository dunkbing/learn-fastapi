from fastapi import FastAPI, Request
import time
from .database import Base, engine
from .user import views as user_views
from .item import views as item_views

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

app.include_router(user_views.user_router, prefix='/users', tags=['users'])
app.include_router(item_views.item_router, prefix='/items', tags=['items'])


@app.get("/")
async def root():
    return {"message": "Hello World"}
