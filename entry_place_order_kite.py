import aiohttp
import asyncio
from datetime import datetime
from payloads.entry_payloads import entry_payloads

api_key = "wejdamed8baj4kpq"

with open("access_token.txt", "r") as f:
    access_token = f.read().strip()

url = "https://api.kite.trade/orders/regular"

headers = {
    "X-Kite-Version": "3",
    "Authorization": f"token {api_key}:{access_token}"
}

def wait_until_exact(hour, minute, second, microsecond):
    target = datetime.now().replace(hour=hour, minute=minute, second=second, microsecond=microsecond)
    if target <= datetime.now():
        return
    while True:
        now = datetime.now()
        if now >= target:
            break

async def post_order(session, payload):
    async with session.post(url, headers=headers, data=payload) as resp:
        await resp.json()

async def main():
    print(f"{datetime.now()} | Placing entry orders")
    wait_until_exact(9, 15, 0, 0)
    async with aiohttp.ClientSession() as session:
        tasks = [post_order(session, payload) for payload in entry_payloads]
        await asyncio.gather(*tasks)
    print(f"{datetime.now()} | All entry orders placed")

if __name__ == "__main__":
    asyncio.run(main())
