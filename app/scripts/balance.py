import json

import aiohttp
import aiofiles

async def get_balance(user_name):
    
    file_path = f"/credentials/{user_name}.json"  # JSON 파일 경로
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        data = await file.read()
        data = json.loads(data)

    base_url = "https://openapi.koreainvestment.com:9443"
    path = "uapi/overseas-stock/v1/trading/inquire-balance"
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
        "CANO": data.get("CANO",""),
        "ACNT_PRDT_CD": data.get("ACNT_PRDT_CD",""),
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "00",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params, timeout=300) as res:
            return await res.json()