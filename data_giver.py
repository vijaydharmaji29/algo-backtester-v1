import numpy as np
import pandas as pd
import brain
import data_collection as dc
import executioner as ex
import csv

all_tickers = []
all_data = {}
position_tickers = []
capital = 10000
icap = capital
all_actions = []
period = 1


with open('nifty50') as f:
    lines = f.readlines()

#sending data of all stocks
for t in lines:
    ticker = t[:-1] + ".NS"
    all_data[ticker] = dc.stock_data(ticker)
    all_tickers.append(ticker)

len_max = len(all_data['NESTLEIND.NS'])


def next_stocks(index):
    if index < len_max:
        data = {
            'Open': [],
            'High': [], 'Low': [],
            'Close': [], 'Volume': [],
            'Dividends': [], 'Stock Splits': [],
            'Momentum': [], '20_ma': [],
            '200_ma': [], '100_ma': [],
            'move': [], 'up': [],
            'down': [], 'average_gain': [],
            'average_loss': [], 'rsi': []
        }

        df = pd.DataFrame(data)
        for ticker in all_tickers:
            current_data = all_data[ticker].iloc[index]
            df.loc[ticker] = np.array(current_data)


        return df

    return None


def cuurent_positions(all_stocks):
    data = {
        'Open': [],
        'High': [], 'Low': [],
        'Close': [], 'Volume': [],
        'Dividends': [], 'Stock Splits': [],
        'Momentum': [], '20_ma': [],
        '200_ma': [], '100_ma': [],
        'move': [], 'up': [],
        'down': [], 'average_gain': [],
        'average_loss': [], 'rsi': []
    }
    positions = pd.DataFrame(data)
    for ticker in position_tickers:
        positions.loc[ticker] = np.array(all_stocks.loc[ticker])


    return positions


def next(index):
    all_stocks = next_stocks(index)
    all_positions = cuurent_positions(all_stocks)

    if index < len_max - 1:
        execute = brain.next(all_stocks, all_positions, capital)
        return execute

    return None

def portfolio_val(position_tickers, index):
    print("Capital: ", capital)
    val = 0
    for i in position_tickers:
        val += all_data[i].iloc[index]['Close']

    cagr = ((((capital + val)/icap ) ** (1/period)) - 1) * 100

    print("Equity Value: ", val)
    print("CAGR: ", cagr)



i = 0
while True:
    print("INDEXING AT -", i)
    execute = next(i)
    if execute:
        position_tickers, capital, executed = ex.trade(execute, capital, position_tickers)
        print(position_tickers)
        for e in executed:
            all_actions.append(e)

    else:
        portfolio_val(position_tickers, i - 1)
        break

    i += 1

# writing to csv file
with open('actions.csv', 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the data rows
    csvwriter.writerows(all_actions)

