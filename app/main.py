from typing import Union
from middleware.auth import AuthMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from scripts import balance

app = FastAPI()

# add middleware
app.add_middleware(AuthMiddleware)

#main code
@app.get("/")
async def get_data():
    return {"this is open-api.yangarch.net"}

@app.get("/balance")
async def check_balance(user_name: str):
    result = await balance.get_balance(user_name)
    return {"result": result}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse('/favicon.ico')

@app.post("/post")
async def post_data(request: Request):
    ...
    return {request}
