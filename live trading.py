import pandas as pd
import sqlalchemy
from binance import AsyncClient
import config


client = AsyncClient(config.api_key, config.api_secret)
engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
df = pd.read_sql('BTCUSDT', engine)
#print(df)

# trend following stratigy
#if the crypto was rising by x % ->Buy same to entry
#exit when profit is above 0.15% or loss is crossing -0.05%


def strategy(entry, lookback, qty, open_position=False):

    while True:
        df = pd.read_sql('BTCUSDT', engine)
        #just filtering the period we are looking for
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.price.pct_change() + 1).cumprod() - 1
        if not open_position:
            #just taking the last row and compare it to the entry
            if cumret[cumret.last_valid_index()] > entry:
                order = client.create_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=qty)
                print(order)
                open_position = True
                break

    if open_position:
        while True:
            df = pd.read_sql('BTCUSDT', engine)
            #filtering after buying the asset
            sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'], unit='ms')]
            if len(sincebuy) > 1:
                sincebuyret = (sincebuy.price.ptc_change() + 1).cumprod() - 1
                last_entry = sincebuyret[sincebuyret.last_valid_index()]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    order = client.create_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=qty)
                    print(order)
                    break


strategy(0.001, 100, 0.0005)
