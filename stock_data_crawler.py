import pandas as pd
import requests
import time


class StockDataCrawler():

    def __init__(self):

        self.period1_timestamp = self.create_timestamp_from_today(-10*30)
        self.period2_timestamp = self.create_today_timestamp()

    def create_today_timestamp(self):
        today = time.strftime("%Y-%m-%d",time.gmtime())
        return int(time.mktime(time.strptime(today, "%Y-%m-%d")))

    def create_timestamp_from_today(self, n):
        today = self.create_today_timestamp()
        return today + n*24*3600

    def get_stock_df(self, ticker):

        ticker = str(ticker) + '.TW'
        
        print('## Info: Download Ticker ' + ticker + '!')
        period1_timestamp = self.period1_timestamp
        period2_timestamp = self.period2_timestamp

        site = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1_timestamp}&period2={period2_timestamp}&interval=1d"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(site, headers=headers).json()

        try:
            result = response["chart"]["result"][0]
            timestamps = result["timestamp"]
            indicators = result["indicators"]["quote"][0]

            stock_df = pd.DataFrame({
                "Ticker": ticker,
                "Date": pd.to_datetime(timestamps, unit="s"),
                "Open": indicators["open"],
                "High": indicators["high"],
                "Low": indicators["low"],
                "Close": indicators["close"],
                "Volume": indicators["volume"]
            })
        
        except:
            stock_df = pd.DataFrame()
            print('## Warning: Ticker ' + ticker + ' is failed!')
        
        return stock_df

    def check_ticker_list_valid(self, ticker_list):

        def check_ticker_valid(ticker):
            import requests

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers).json()

            return r.get("chart", {}).get("error") is None

        valid_count = 0
        valid_ticker_list = []
        for name in ticker_list:
            if check_ticker_valid(name):
                valid_count += 1
                valid_ticker_list.append(name)

        return valid_count, valid_ticker_list
