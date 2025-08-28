import os
import requests
import asyncio
import aiohttp
from datetime import datetime
from payloads.exit_payload import exit_payloads

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

async def modify_order(session, api_key, access_token, order_id, payload):
    url = f"https://api.kite.trade/orders/regular/{order_id}"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}",
    }
    data = {
        "order_type": payload["order_type"],
        "quantity": payload["quantity"],
        "price": payload["price"],
        "validity": payload["validity"],
        "tradingsymbol": payload["tradingsymbol"],
        "exchange": payload["exchange"],
        "transaction_type": payload["transaction_type"],
        "product": payload["product"],
    }
    async with session.put(url, headers=headers, data=data) as resp:
        await resp.text()

async def modify_orders_async(api_key, access_token, order_map):
    async with aiohttp.ClientSession() as session:
        tasks = [
            modify_order(session, api_key, access_token, oid, payload)
            for oid, payload in order_map.items()
        ]
        await asyncio.gather(*tasks)

def filter_and_modify(api_key, access_token, orders, payloads):
    order_map = {}
    for order in orders:
        if order.get("status") == "OPEN" and (order.get("tag") or "") == "eprs_2_ex":
            for payload in payloads:
                if (
                    order["tradingsymbol"] == payload["tradingsymbol"]
                    and order["transaction_type"] == payload["transaction_type"]
                ):
                    order_map[order["order_id"]] = payload
                    break
    if order_map:
        asyncio.run(modify_orders_async(api_key, access_token, order_map))

if __name__ == "__main__":
    with open(ACCESS_TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()
    orders = get_orders(API_KEY, ACCESS_TOKEN)
    filter_and_modify(API_KEY, ACCESS_TOKEN, orders, exit_payloads)
    print(f"{datetime.now()} - Exit orders modified with latest payloads")
