import os
import json
import requests
import pyotp
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect

API_KEY = "wejdamed8baj4kpq"
API_SECRET = "peho35kz7k50x2gw8ycn5rdjmrd75mri"
USER_ID = "DXU151"
USER_PASSWORD = "Pratibha"
TOTP_KEY = "FLJBDJNEBOIMZZZPE25YYYR72Y2B2IAP"
ACCESS_TOKEN_FILE = "access_token.txt"

def get_request_token(session):
    login_url = f"https://kite.trade/connect/login?v=3&api_key={API_KEY}"
    session.get(url=login_url)
    response = session.post(
        url="https://kite.zerodha.com/api/login",
        data={"user_id": USER_ID, "password": USER_PASSWORD}
    )
    resp_dict = response.json()
    session.post(
        url="https://kite.zerodha.com/api/twofa",
        data={
            "user_id": USER_ID,
            "request_id": resp_dict["data"]["request_id"],
            "twofa_value": pyotp.TOTP(TOTP_KEY).now()
        }
    )
    final_url = f"{login_url}&skip_session=true"
    redirected_url = session.get(final_url, allow_redirects=True).url
    request_token = parse_qs(urlparse(redirected_url).query)["request_token"][0]
    return request_token

def save_access_token(token):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ACCESS_TOKEN_FILE)
    with open(path, "w") as f:
        f.write(token)

def login():
    session = requests.Session()
    request_token = get_request_token(session)
    kite = KiteConnect(api_key=API_KEY)
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    kite.set_access_token(data["access_token"])
    save_access_token(data["access_token"])
    return kite

if __name__ == "__main__":
    kite = login()
    print(f"{datetime.now()} - Login Successful")
    print(kite.profile())
