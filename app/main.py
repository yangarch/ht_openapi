from typing import Union
from middleware.auth import AuthMiddleware
from fastapi import FastAPI, Request

app = FastAPI()

# add middleware
app.add_middleware(AuthMiddleware)

#main code
@app.get("/")
async def get_data():
    return {"this is open-api.yangarch.net"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/post")
async def post_data(request: Request):
    ...
    return {request}


"""
ADD user API


"""