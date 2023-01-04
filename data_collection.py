import yfinance as yf
import numpy as np
from scipy.stats import linregress

global final_data

def calculate_momentum(data, period):
    close = np.array(data.Close)
    momentums = []

    for i in range(len(close)):
        if i < period:
            momentums.append(None)
            continue

        y_data = np.log(close[i-period: i])
        x_data = np.arange(period)
        beta, _, rvalue, _, _ = linregress(x_data, y_data)
        momentums.append(((1 + beta) ** 252) * (rvalue ** 2))

    data['Momentum'] = momentums


def stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1y', interval='60m', auto_adjust = True)

    calculate_momentum(data, 90)
    data["20_ma"] = data["Close"].ewm(span=20).mean()
    data["200_ma"] = data["Close"].ewm(span=200).mean()
    data["100_ma"] = data["Close"].ewm(span=20).mean()
    data['move'] = data['Close'] - data['Close'].shift(1)
    data['up'] = np.where(data['move'] > 0, data['move'], 0)
    data['down'] = np.where(data['move'] < 0, data['move'], 0)
    data['average_gain'] = data['up'].rolling(14).mean()
    data['average_loss'] = data['down'].abs().rolling(14).mean()
    relative_strength = data['average_gain'] / data['average_loss']
    data['rsi'] = 100.0 - (100.0 / (1.0 + relative_strength))

    data = data.dropna()

    return data
