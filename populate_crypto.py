import config, requests
import sqlite3

connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    SELECT * FROM crypto
""")
rows = cursor.fetchall()


#url = f'{config.BASE_URL_NOMICS}/currencies/ticker?key={config.API_KEY_NOMICS}'

# requesteddata = requests.get(url)
# json_data = requesteddata.json()
# cursor.execute(f'''
#     SELECT id FROM crypto
# ''')
# current_ids = cursor.fetchall()
# for coin in json_data:
#     name = coin['name'] 
#     symbol = coin['symbol']
#     if symbol not in current_ids:
#         try:
#             print(f'Adding {name}, {symbol}', coin['price'])
#             cursor.execute(f'''INSERT INTO crypto (symbol, name) VALUES ('{symbol}', '{name}')''')
#             cursor.execute(f'''INSERT INTO crypto_price (crypto_id, date, price, market_cap, supply, rank) VALUES
#             ('{symbol}','{coin['price_date']}', '{coin['price']}', '{coin['market_cap']}', 
#             '{coin['circulating_supply']}', '{coin['rank']}')''')

#         except:
#             pass

cursor.execute(f'''
    SELECT id, symbol FROM crypto ORDER BY id
''')
rows = cursor.fetchall()
current_symbols = [row['symbol'] for row in rows]
for symbol in current_symbols:
    try:
        url = f'{config.BASE_URL_COMP}data/v2/histoday?fsym={symbol}&tsym=USD&limit=2&api_key={config.API_KEY_COMP}'
        requesteddata = requests.get(url)
        json_data = requesteddata.json()
        data = json_data['Data']['Data']
    except:
        continue
    
    for day in data:
        cursor.execute(f'''INSERT INTO crypto_OHLCV (crypto_id, date, high, low, open, close, volumeto, volumefor)
        VALUES ('{symbol}','{day['time']}','{day['high']}','{day['low']}','
        {day['open']}','{day['close']}','{day['volumeto']}','{'volumefrom'}')''')
        print(symbol)

async def request_pull

connection.commit()

