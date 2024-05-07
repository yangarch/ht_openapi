import json

import aiohttp
import aiofiles


async def buy(user_name, pdno, dvsn, qty, unpr):
        
    file_path = f"/credentials/{user_name}.json"  # JSON 파일 경로
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        data = await file.read()
        data = json.loads(data)

    base_url = "https://openapi.koreainvestment.com:9443"
    path = "/uapi/domestic-stock/v1/trading/order-cash" #path 수정
    url = f"{base_url}/{path}"

    headers = {
        "content-type": "application/json; charset=utf-8",
        "Authorization": f'Bearer {data.get("access_token","")}',
        "appkey": data.get("appkey",""),
        "appsecret": data.get("appsecret",""),
        "tr_id":"TTTC8434R",
        "tr_cont": "",
        "custtype": "P",
    }

    params = {
        "CANO": data.get("CANO",""), #계좌앞자리
        "ACNT_PRDT_CD": data.get("ACNT_PRDT_CD",""), #계좌뒷자리
        "PDNO": pdno,#종목코드
        "ORD_DVSN": dvsn,#주문 구분
        "ORD_QTY": qty, # 주문 수량
        "ORD_UNPR": unpr, # 주문 단가
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params, timeout=300) as res:
            return await res.json()