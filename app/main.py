from typing import Union
from middleware.auth import AuthMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from scripts import balance, trade, price

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# add middleware
app.add_middleware(AuthMiddleware)

#main code
@app.get("/")
async def get_data():
    return {"this is open-api.yangarch.net"}

@app.get("/v1/{endpoint:path}") # 미구현
async def forward_api_request(endpoint: str, request: Request, user_name: str):
    # 인증은 미들웨어에서 처리되고 여기에서는 API 요청을 전달합니다.
    params = dict(request.query_params)
    params.pop('user_name', None)  # 원본 요청에서 user_name을 제거

    # 실제 요청할 외부 API의 기본 URL
    external_api_base_url = "https://api.external.com"
    
    # httpx를 이용하여 외부 API 호출
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{external_api_base_url}/{endpoint}", params=params)
    
    return JSONResponse(status_code=response.status_code, content=response.json())

@app.get("/balance")
async def check_balance(user_name: str):
    result = await balance.get_balance(user_name)
    return {"result": result}

@app.get("/buy")
async def buy(user_name: str, pdno: str, dvsn: str, qty: str, unpr: str):
    print(f"call buy by {user_name}")
    result = await trade.buy(user_name, pdno, dvsn, qty, unpr)
    return {"result": result}

@app.get("/sell")
async def sell(user_name: str, pdno: str, dvsn: str, qty: str, unpr: str):
    print(f"call sell by {user_name}")
    result = await trade.sell(user_name, pdno, dvsn, qty, unpr)
    return {"result": result}

@app.get("/current_price")
async def price(user_name: str, iscd: str):
    print(f"call price {user_name}")
    result = await price.current_price(user_name, iscd)
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
