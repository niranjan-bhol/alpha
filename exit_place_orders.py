import aiohttp
import asyncio
from datetime import datetime
from payloads.exit_payload import exit_payloads

api_key = "wejdamed8baj4kpq"

with open("access_token.txt", "r") as f:
    access_token = f.read().strip()

url = "https://api.kite.trade/orders/regular"

headers = {
    "X-Kite-Version": "3",
    "Authorization": f"token {api_key}:{access_token}"
}

async def post_order(session, payload):
    async with session.post(url, headers=headers, data=payload) as resp:
        await resp.json()

async def main():
    print(f"{datetime.now()} | Placing exit orders")
    async with aiohttp.ClientSession() as session:
        tasks = [post_order(session, payload) for payload in exit_payloads]
        await asyncio.gather(*tasks)
    print(f"{datetime.now()} | All exit orders placed")

if __name__ == "__main__":
    asyncio.run(main())