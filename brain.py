import math

class action(object):
    def __init__(self, ticker, buy, sell, buy_val, sell_val):
        self.ticker = ticker
        self.buy = buy
        self.sell = sell
        self.buy_val = buy_val
        self.sell_val = sell_val

    def show(self):
        print(self.ticker, self.buy,
              self.sell, self.buy_val, self.sell_val)

def next(stocks, positions, capital):
    # print(positions.index)
    sorted_stocks = stocks.sort_values('Momentum')
    sorted_stocks = sorted_stocks[:10] #how to slice pandas dataframe

    execute = []
    x = capital * math.pow(2,10)/(math.pow(2,11) - 2)
    tickers_top20 = []

    #figuring out long positions
    i = 0
    for ticker, row in sorted_stocks.iterrows():

        if (ticker not in positions.index) and row["20_ma"] > row["200_ma"]:
            tickers_top20.append(ticker)
            buy_val = x / (math.pow(2, i + 1))
            new_action = action(ticker, True, False, buy_val, 0)
            execute.append(new_action)
        elif row["100_ma"] < row["Close"] and row['rsi'] >= 30 and row["20_ma"] > row["200_ma"]: # for hold
            if ticker in positions.index:
                tickers_top20.append(ticker)
                execute.append(action(ticker, False, False, 0, 0))

        i+=1

    #figuring out short positions:
    for ticker, row in positions.iterrows():
        if ticker not in tickers_top20 or row["100_ma"] > row["Close"] or row['rsi'] < 30 and row["20_ma"] < row["200_ma"]:
            # short
            new_action = action(ticker, False, True, 0, row['Close'])
            execute.append(new_action)



    return execute
