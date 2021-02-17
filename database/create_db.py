import sqlite3, config

connection = sqlite3.connect(config.DB_PATH)

cursor = connection.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL UNIQUE,
            company TEXT NOT NULL,
            exchange TEXT NOT NULL)""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_price (
            id INTEGER PRIMARY KEY,
            stock_id INTEGER,
            date NOT NULL, 
            open NOT NULL,
            high NOT NULL,
            low NOT NULL,
            close NOT NULL,
            volume NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id)
        )""")
    
cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto(
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE
        )""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_price(
            id INTEGER PRIMARY KEY,
            crypto_id TEXT NOT NULL,
            date NOT NULL,
            price NOT NULL,
            market_cap NOT NULL,
            supply NOT NULL,
            rank NOT NULL,
            FOREIGN KEY (crypto_id) REFERENCES crypto (id)
        )
""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_OHLCV(
            id INTEGER PRIMARY KEY,
            crypto_id TEXT NOT NULL,
            date NOT NULL,
            high NOT NULL,
            low NOT NULL,
            open NOT NULL,
            close NOT NULL,
            volumeto NOT NULL,
            volumefor NOT NULL,
            FOREIGN KEY (crypto_id) REFERENCES crypto (id)
        )
""")
connection.commit()