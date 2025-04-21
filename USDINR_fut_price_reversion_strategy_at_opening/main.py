from calc_e import get_e_value
from usd_rate_fetcher import USDRateFetcher
from inr_rate_fetcher import INRRateFetcher
from fetch_spot_price_cnbc import SpotPriceFetcherCNBC
from fetch_spot_price_bloomberg import SpotPriceFetcherBloomberg
from expiry_dates import USDINRExpiryDates2025
from fetch_time_to_expiry import TimeToExpiryCalculator
from datetime import datetime

def main():

    print()

    e_value = get_e_value()
    print(f"The value of Euler's number (e) is: {e_value}")

    print()

    days_remaining = TimeToExpiryCalculator.calculate_days_to_expiry()
    print(f"Days to expiry for this month's USDINR futures contract: {days_remaining}")

    print()

    fetcher = USDRateFetcher()
    latest_int_rate = fetcher.fetch_term_sofr_1month_rate()
    
    if latest_int_rate:
        print(f"The latest Term SOFR (1-month) is: {latest_int_rate} %")
    #else:
        #print("Could not fetch the 1-month term SOFR.")
    
    print()

    fetcher = INRRateFetcher()
    mibor_14d_rate, mibor_1m_rate, mibor_3m_rate, date = fetcher.fetch_term_mibor_rates()
    
    print(f"MIBOR Rates | {date}")
    print(f"var1 : 14 Days  : {mibor_14d_rate} %")
    print(f"var2 : 1 Month  : {mibor_1m_rate} %")
    print(f"var3 : 3 Months : {mibor_3m_rate} %")

    print()

    spot_price_fetcher = SpotPriceFetcherCNBC()
    
    last_trade_time, last_price = spot_price_fetcher.fetch_data()
    
    if last_trade_time and last_price is not None:
        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"USDINR Spot Data CNBC | {formatted_datetime}")
        print(f"Data Timestamp (on CNBC page): {last_trade_time}")
        print(f"Last Price: {last_price:.4f}")
    else:
        print("Could not fetch any spot price data.")

    print()

    spot_price_fetcher_bloomberg = SpotPriceFetcherBloomberg()
    spot_price_fetcher_bloomberg.fetch_data()
    
    price = spot_price_fetcher_bloomberg.get_price()
    timestamp = spot_price_fetcher_bloomberg.get_timestamp()
    
    if last_trade_time and last_price is not None:
        now = datetime.now()
        formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"USDINR Spot Data Bloomberg | {formatted_datetime}")
        print(f"Data Timestamp (on Bloomberg page): {timestamp}")
        print(f"Last Price: {price}")
    else:
        print("Could not fetch any spot price data.")

    print()

    e = e_value
    T = days_remaining/365
    r_f = latest_int_rate/100
    r_d = mibor_1m_rate/100
    S_cnbc = last_price
    #S_cnbc = 85.6543
    S_bloomberg = price
    #S_bloomberg = 85.9876
    
    F_cnbc = S_cnbc * e ** ((r_d - r_f) * T)
    F_bloom = S_bloomberg * e ** ((r_d - r_f) * T)
    
    print(f"Fair price of USDINR CNBC: {F_cnbc:.4f}")
    print(f"Fair price of USDINR Bloomberg : {F_bloom:.4f}")

    print()

if __name__ == "__main__":
    main()
