#This is running with chronjobs every day at 11pm
#Populates the DB with names and symbols of companies
from database import config
import sqlite3 
import requests

connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    SELECT symbol, company FROM stock
""")
rows = cursor.fetchall()

current_symbols = [row['symbol'] for row in rows]

data_with_symbolname = f"{config.BASE_URL}beta/ref-data/symbols?token={config.API_KEY}"

requesteddata = requests.get(data_with_symbolname)
json_data = requesteddata.json()
for i in range(len(json_data)):
    try:
        symbol = json_data[i]['symbol']
        if symbol not in current_symbols:
            company = json_data[i]['name']
            exchange = json_data[i]['exchange']
            if exchange == 'NAS':
                exchange = 'NASDAQ'
            elif exchange == 'NYE':
                exchange = 'NYSE'
            else:
                continue
            cursor.execute(f'''INSERT INTO stock (symbol, company, exchange) VALUES ('{symbol}', 
                        '{company}', '{exchange}')''')
            print(f'New stock added: {company} with symbol: {symbol} and exchange {exchange}')
    except:
        pass

print('The job is completed!')
connection.commit()




