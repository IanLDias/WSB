from database import config
import requests
import sqlite3
import asyncio

import asyncio
import logging

import aiohttp
from aiohttp import ClientSession

connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    SELECT * FROM crypto
""")
rows = cursor.fetchall()
current_symbols = [row['symbol'] for row in rows]

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

async def request_pull(symbol, session:ClientSession):
    url = f'{config.BASE_URL_COMP}data/v2/histoday?fsym={symbol}&tsym=USD&limit=2000&api_key={config.API_KEY_COMP}'
    resp = await session.request(method="GET", url=url)
    json_data = await resp.json()
    try:
        data = json_data['Data']['Data']
        return data
    except:
        pass
    

async def writing_sql(data, symbol):
    for day in data:
        print(symbol)
        cursor.execute(f'''INSERT INTO crypto_OHLCV (crypto_id, date, high, low, open, close, volumeto, volumefor)
        VALUES ('{symbol}','{day['time']}','{day['high']}','{day['low']}','
        {day['open']}','{day['close']}','{day['volumeto']}','{day['volumefrom']}')''')
        

async def chain(symbol):
    try:
        async with ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            p1 = await request_pull(symbol, session=session)
            if p1:
                p2 = await writing_sql(data=p1, symbol=symbol)
    except:
        pass

async def main():
    await asyncio.gather(*(chain(symbol) for symbol in current_symbols))
    

asyncio.run(main())
connection.commit()

