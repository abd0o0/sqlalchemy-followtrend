import pandas as pd
import asyncio
from binance import AsyncClient, BinanceSocketManager
import config
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')


async def main():
    client = AsyncClient(config.api_key, config.api_secret)
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket('BTCUSDT')
    while True:
        await socket.__aenter__()
        msg = await socket.recv()
        df = createframe(msg)
        df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
        print(df)


def createframe(msg):
   df = pd.DataFrame([msg])
   df = df.loc[:, ['s', 'E', 'p']]
   df.columns = ['symbol', 'Time', 'price']
   df.price = df.price.astype(float)
   df.Time = pd.to_datetime(df.Time, unit='ms')

   return df


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
