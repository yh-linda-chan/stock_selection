
# Library
import numpy as np

class StockEvaluator():

    def __init__(self):

        self.close_ma_percent = 0.05
        self.min_volume = 200000
        self.high_close_percent = 0.01

        self.buy_sign_count = 2


    def procss(self, ticker, stock_df):

        ticker = str(ticker) + '.TW'

        stock_df['MA5'] = stock_df['Close'].rolling(window=5, min_periods=1).mean()
        stock_df['MA10'] = stock_df['Close'].rolling(window=10, min_periods=1).mean()
        stock_df['MA20'] = stock_df['Close'].rolling(window=20, min_periods=1).mean()
        stock_df['MA60'] = stock_df['Close'].rolling(window=60, min_periods=1).mean()

        stock_df['index'] = stock_df[['MA5', 'MA10', 'MA20', 'MA60']].max(axis=1)

        # 四海遊龍
        stock_df['Signal_1'] = np.where(stock_df['Close'] >= stock_df['index'], 1, 0)

        # MA5大於MA20
        stock_df['Signal_2'] = np.where(stock_df['MA5'] >= stock_df[['MA20']].max(axis=1), 1, 0)

        # 收盤不能大於MA %
        stock_df['Signal_3'] = np.where((stock_df['Close']-stock_df['index'])/stock_df['index'] < self.close_ma_percent, 1, 0)

        # 成交量大於1000
        stock_df['Signal_4'] = np.where(stock_df['Volume'] >= self.min_volume, 1, 0)

        # buy signal
        stock_df['buy_sign'] = np.where(stock_df[['Signal_1', 'Signal_2', 'Signal_3', 'Signal_4']].sum(axis=1) == 4, 1, 0)

        stock_df['buy'] = stock_df['buy_sign'].rolling(window=self.buy_sign_count).apply(lambda x: 1 if all(x == 1) else 0, raw=True).fillna(0).astype(int)

        # *當日最高價不能大於收盤價 % 
        # stock_df['Signal_5'] = np.where((stock_df['High']-stock_df['Close'])/stock_df['Close'] < high_close_percent, 1, 0)

        output = self.check_sign(str(ticker), stock_df)

        return output
    

    def check_sign(self, ticker, stock_df):

        if stock_df['buy'].iloc[-1] == 1 :

            # print('Select ' + ticker + '!')
            return f'Good Sign {ticker}'
            # return [ticker, float(stock_df['Close'][-1:])]

        else:

            return f'Please Wait {ticker}'
            # return []
