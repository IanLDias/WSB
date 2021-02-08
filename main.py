import sqlite3 
import requests, config

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/stocks")
def stocks(request: Request):
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, company FROM stock
        WHERE id IN (SELECT DISTINCT stock_id FROM stock_price)
    """)
    rows = cursor.fetchall()

    return templates.TemplateResponse("base_stocks.html", {"request": request, "stocks": rows})

@app.get("/stocks/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, company, exchange FROM stock WHERE symbol = ?
    """, (symbol,))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """,(row['id'],))

    prices = cursor.fetchall()
     
    return templates.TemplateResponse("individual_stock.html", {"request": request, "stock": row, "prices":prices})
    return symbol 

@app.get("/crypto")
def crypto(request: Request):
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM crypto
    """)
    rows = cursor.fetchall()
    return templates.TemplateResponse("base_crypto.html", {"request": request, "all_crypto": rows})

@app.get("/crypto/{symbol}")
def crypto_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM crypto WHERE symbol = '{symbol}'
    """)
    row = cursor.fetchone()

    cursor.execute(f"""
    SELECT * FROM crypto_price
    WHERE crypto_id = '{symbol}'
    GROUP BY crypto_id
    """)
    prices = cursor.fetchall()

    return templates.TemplateResponse("individual_crypto.html", {"request": request, "crypto": row, "prices":prices})