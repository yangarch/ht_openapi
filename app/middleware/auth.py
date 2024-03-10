import aiofiles
import json
from datetime import datetime

import aiohttp
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


async def get_access_token(user_name=None):
    """
    read file and check date and renew
    """
    # JSON 파일을 열고 읽기
    file_path = f"/credentials/{user_name}.json"  # JSON 파일 경로
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        data = await file.read()
        data = json.loads(data)

    access_token_token_expired = data.get("access_token_token_expired", "")
    current_time = datetime.now()
    expired_time = current_time

    if access_token_token_expired != "":
        expired_time = datetime.strptime(access_token_token_expired, "%Y-%m-%d %H:%M:%S")

    if expired_time <= current_time or access_token_token_expired == "":
        await renew_accees_token(data)


async def renew_accees_token(data):
    user_name = data.get("user_name", "")
    appkey = data.get("appkey", "")
    appsecret = data.get("appsecret", "")
    access_token = data.get("access_token_token", "")
    access_token_token_expired = data.get("access_token_token_expired", "")

    url = "https://openapi.koreainvestment.com:9443"
    body = {"grant_type": "", "appkey": appkey, "appsecret": appsecret}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(body), timeout=300) as res:
            result = await res.json()
            access_token = result.get("access_token", "")
            access_token_token_expired = result.get("access_token_token_expired", "")

    data["access_token"] = access_token
    data["access_token_token_expired"] = access_token_token_expired

    # JSON 데이터를 새 파일로 덮어쓰기
    file_path = f"/credentials/{user_name}.json"  # 파일 경로 지정
    async with aiofiles.open(file_path, mode="w", encoding="utf-8") as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))


# Middleware 에서 token 발급
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_name = ""
        if request.method == "POST":
            try:
                # POST 요청일 경우, JSON 에서 parsing
                request_data = await request.json()
                user_name = request_data.get("user_name", "")
            except Exception as e:
                # JSON 본문이 없는 경우 처리
                request_data = {"error": str(e)}
        elif request.method == "GET":
            # GET 요청일 경우, 쿼리 파라미터 로깅
            request_data = dict(request.query_params)
            user_name = request_data.get("user_name", "")

        # log_data 함수 호출
        print(f"user_name :{user_name}")
        await get_access_token(user_name)

        response = await call_next(request)
        return response
