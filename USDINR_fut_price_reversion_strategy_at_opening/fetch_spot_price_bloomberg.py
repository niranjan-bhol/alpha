from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from typing import Optional, Tuple

class SpotPriceFetcherBloomberg:
    def __init__(self):
        self.url = "https://www.bloomberg.com/quote/USDINR:CUR"
        self.price: Optional[float] = None
        self.timestamp: Optional[str] = None

    def fetch_data(self) -> Tuple[Optional[str], Optional[float]]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/118.0.5993.90 Safari/537.36"
                    )
                )
                page = context.new_page()
                page.goto(self.url, wait_until="domcontentloaded", timeout=20000)

                # --- PRICE FETCHING ---
                page.wait_for_selector("div[data-component='sized-price']", timeout=15000)
                price_elements = page.query_selector_all("div[data-component='sized-price']")
                if price_elements:
                    for elem in price_elements:
                        try:
                            visible = elem.is_visible()
                            text = elem.inner_text().strip()
                            if visible and text.replace(",", "").replace(".", "").isdigit():
                                float_val = float(text.replace(",", ""))
                                if 70 < float_val < 100:
                                    self.price = float_val
                                    break
                        except:
                            continue

                # --- TIMESTAMP FETCHING ---
                time_element = page.query_selector("time.timestamp_timeStamp__oD1aI")
                if time_element:
                    self.timestamp = time_element.inner_text().strip()

                browser.close()

        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_price(self):
        return self.price

    def get_timestamp(self):
        return self.timestamp
