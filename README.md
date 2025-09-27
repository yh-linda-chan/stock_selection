# Stock Selection Testing
stock selection by indicators. No responsibility for stock selection results.

# Example

```python
import stock_data_crawler
import stock_evaluator

# 初始化物件
stock_data_crawler = stock_data_crawler.StockDataCrawler()
stock_evaluator = stock_evaluator.StockEvaluator()

# 指定股票代號
ticker = '2330.TW'

# 抓取股票資料
stock_df = stock_data_crawler.get_stock_df(ticker)

# 進行評估
stock_evaluator.procss(ticker, stock_df)
