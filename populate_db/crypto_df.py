import sqlite3 
import requests, config
import pandas as pd
import pickle

connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    SELECT DISTINCT crypto_id FROM crypto_OHLCV
""")
rows = cursor.fetchall()
current_symbols = [row['crypto_id'] for row in rows]
all_dfs = []

for symbol in current_symbols:
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM crypto_OHLCV
        WHERE crypto_id = '{symbol}'
    """)
    rows = cursor.fetchall()
    keys = rows[0].keys()
    df = pd.DataFrame.from_records(rows, index='id', columns = keys)
    all_dfs.append(df)

#pickle.dump(all_dfs, open('list_crypto.pkl', 'wb'))
