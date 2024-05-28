import json

import aiohttp
import aiofiles

async def current_price(user_name, iscd):
    file_path = f"/credentials/{user_name}.json"  # JSON 파일 경로
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        data = await file.read()
        data = json.loads(data)

    base_url = "https://openapi.koreainvestment.com:9443"
    path = "uapi/domestic-stock/v1/quotations/inquire-price" #path 수정
    url = f"{base_url}/{path}"

    headers = {
        "Authorization": f'Bearer {data.get("access_token","")}',
        "appkey": data.get("appkey",""),
        "appsecret": data.get("appsecret",""),
        "tr_id":"FHKST01010100",
        "custtype": "P",
    }

    params = {
        "FID_COND_MRKT_DIV_CODE":"J",
        "FID_INPUT_ISCD": iscd,#종목코드
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=json.dumps(params), timeout=300) as res:
            return await res.json()