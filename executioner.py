def trade(execute, capital, positions):
    position_tickers = []
    executed = []
    capital = capital
    ctr = 0
    for e in execute:
        print("EXECUTING: - ", ctr)
        if e.buy and not e.sell and capital >= e.buy_val and capital > 0:
            capital -= e.buy_val
            position_tickers.append(e.ticker)
            print("BOUGHT -", e.ticker, " -", e.buy_val)
            executed.append(('BOUGHT', e.ticker, e.buy_val, capital))
        elif not e.buy and e.sell:
            capital += e.sell_val
            print("SOLD -", e.ticker, " -", e.sell_val)
            executed.append(('SOLD', e.ticker, e.sell_val, capital))
        elif not e.buy and not e.sell and e.ticker in positions:
            position_tickers.append(e.ticker)
            print("HOLDING -", e.ticker)
            executed.append(('HOLDING', e.ticker, 0, capital))
        ctr += 1

    return position_tickers, capital, executed
