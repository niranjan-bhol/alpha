import asyncio
import aiohttp
import pyotp
import requests
from datetime import datetime, time
from payloads.entry_payloads import entry_payloads

KITE_USERNAME = 'DXU151'
KITE_PASSWORD = 'Pratibha'
TOTP_KEY = 'FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP'

enctoken = None

def login_kite():
    global enctoken
    session = requests.Session()
    res1 = session.post(
        'https://kite.zerodha.com/api/login',
        data={
            "user_id": KITE_USERNAME,
            "password": KITE_PASSWORD,
            "type": "user_id"
        }
    )
    request_id = res1.json()['data']['request_id']
    res2 = session.post(
        'https://kite.zerodha.com/api/twofa',
        data={
            "request_id": request_id,
            "twofa_value": pyotp.TOTP(TOTP_KEY).now(),
            "user_id": KITE_USERNAME,
            "twofa_type": "totp"
        }
    )
    enctoken = session.cookies.get_dict()['enctoken']
    print(f"{datetime.now()} | Login Sucessful")

async def place_order(session, order):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://kite.zerodha.com/dashboard",
        "Accept-Language": "en-US,en;q=0.6",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"enctoken {enctoken}"
    }
    url = 'https://kite.zerodha.com/oms/orders/regular'
    async with session.post(url, headers=headers, data=order) as response:
        await response.json()

async def main():
    print(f"{datetime.now()} | Placing entry orders")
    async with aiohttp.ClientSession() as session:
        tasks = [place_order(session, order) for order in entry_payloads]
        await asyncio.gather(*tasks)
    print(f"{datetime.now()} | All entry orders placed")

def schedule_loop():
    #print("Waiting for 09:14:00 to login...")
    while datetime.now().time() < time(9, 14, 0, 0):
        continue
    login_kite()
    #print("Waiting for 09:15:00 to place orders...")
    while datetime.now().time() < time(9, 15, 0, 0):
        continue
    asyncio.run(main())

if __name__ == "__main__":
    schedule_loop()
