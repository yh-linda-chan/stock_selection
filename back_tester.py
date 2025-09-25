class BackTester():

    @staticmethod
    def process(stock_df, initial_cash=100000):

            cash = initial_cash
            position = 0  # 持股數量
            entry_price = 0
            portfolio_values = []

            for i in range(len(stock_df)):
                price = stock_df['Close'].iloc[i]
                buy_signal = stock_df['buy'].iloc[i]

                # --- Buy condition ---
                if buy_signal == 1 and position == 0:
                    position = cash // price   # 全倉買入
                    cash -= position * price
                    entry_price = price
                    # print(f"Buy at {price}")

                # --- Sell condition ---
                elif position > 0:
                    # 出場邏輯：跌破 MA20 就賣
                    if price < stock_df['MA20'].iloc[i]:
                        cash += position * price
                        # print(f"Sell at {price}, Profit={price-entry_price}")
                        position = 0

                # 總資產（現金 + 股票市值）
                portfolio_value = cash + position * price
                portfolio_values.append(portfolio_value)

            # Final
            final_value = portfolio_values[-1]
            return_rate = (final_value - initial_cash) / initial_cash * 100

            return {
                "Initial_Cash": initial_cash,
                "Final_Value": final_value,
                "Return_Rate": return_rate,
                "Portfolio_History": portfolio_values
            }
