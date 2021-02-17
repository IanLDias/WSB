#Populates the DB with prices 
from database import config
import requests
import sqlite3
from datetime import date

today = date.today()
current_date = today.strftime("%Y/%m/%d")
connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    SELECT id, symbol, company FROM stock
""")
rows = cursor.fetchall()

symbols = []
stock_dict = {}

for row in rows:
    symbol = row['symbol']
    if symbol[-1] == '+':
        continue
    symbols.append(symbol)
    stock_dict[symbol] = row['id']


var_list = ['date', 'open', 'high', 'low', 'close', 'volume']

batch_size = 100
for i in range(0, len(symbols), batch_size):
    symbol_batch= symbols[i:i+batch_size]
    price_data = requests.get(f'{config.SB_BASE}v1/stock/market/batch?types=chart&symbols={symbol_batch}&token={config.SB_TOKEN}')
    try:
        price_data_json = price_data.json()
    except:
        continue
    for batch in symbol_batch:
        try:
            ts_data = price_data_json[batch]['chart']
        except:
            continue
        for symbol in ts_data:
            stock_id = stock_dict[symbol['symbol']]
            result_list = [symbol[var] for var in var_list]
            print(stock_id, result_list)
            if not None in result_list:
                cursor.execute(f'''INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                    values ({stock_id}, {result_list[0]}, {result_list[1]}, {result_list[2]}, {result_list[3]}, 
                    {result_list[4]}, {result_list[5]})
                    ''')

connection.commit()