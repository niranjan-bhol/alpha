import requests
import asyncio
import aiohttp
from datetime import datetime

API_KEY = "wejdamed8baj4kpq"
ACCESS_TOKEN_FILE = "access_token.txt"

def get_orders(api_key, access_token):
    url = "https://api.kite.trade/orders"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

async def cancel_order(session, api_key, access_token, order_id):
    url = f"https://api.kite.trade/orders/regular/{order_id}"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}",
    }
    async with session.delete(url, headers=headers) as resp:
        await resp.text()

async def cancel_orders_async(api_key, access_token, order_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [cancel_order(session, api_key, access_token, oid) for oid in order_ids]
        await asyncio.gather(*tasks)

def filter_and_cancel(api_key, access_token, orders):
    order_ids = [
        order["order_id"]
        for order in orders
        if "eprs_1_en" in (order.get("tag") or "") and order.get("status") == "OPEN"
    ]
    if order_ids:
        asyncio.run(cancel_orders_async(api_key, access_token, order_ids))

if __name__ == "__main__":
    with open(ACCESS_TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()

    orders = get_orders(API_KEY, ACCESS_TOKEN)
    filter_and_cancel(API_KEY, ACCESS_TOKEN, orders)
    print(f"{datetime.now()} - All open entry orders are Cancelled")
