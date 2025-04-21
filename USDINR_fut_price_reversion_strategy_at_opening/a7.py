from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def fetch_usdinr_spot():
    url = "https://www.bloomberg.com/quote/USDINR:CUR"
    price = None
    timestamp = None

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
            page.goto(url, wait_until="domcontentloaded", timeout=20000)

            # --- PRICE FETCHING (UNCHANGED) ---
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
                                price = text
                                break
                    except:
                        continue

            # --- TIMESTAMP FETCHING ---
            time_element = page.query_selector("time.timestamp_timeStamp__oD1aI")
            if time_element:
                timestamp = time_element.inner_text().strip()

            browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return price, timestamp


if __name__ == "__main__":
    rate, ts = fetch_usdinr_spot()
    print(f"USD/INR Spot Price: {rate}")
    print(f"Timestamp: {ts}")
