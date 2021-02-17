import sqlite3 
import requests, config

connection = sqlite3.connect(config.DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
cursor.execute("""
    DROP TABLE stock_price""")

cursor.execute("""
    DROP TABLE stock""")

connection.commit()