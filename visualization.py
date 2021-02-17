from database import config
import sqlite3 
import pandas as pd
from datetime import datetime
import mpld3
import plotly.graph_objects as go


connection = sqlite3.connect(config.DB_PATH)
df = pd.read_sql_query("SELECT * FROM crypto_OHLCV", connection)

df.set_index('id', inplace=True)

btc = df[df['crypto_id'] == 'BTC']

def convert_unix_to_datetime(date_col):
    'Converts the unix dates into YYYY-MM-DD'
    int_list = list((map(int,date_col)))
    date_list = list(map(datetime.utcfromtimestamp, int_list))
    converted_dates = [date_list[i].strftime('%Y-%m-%d') for i in range(len(date_list))]
    return converted_dates
converted_dates = convert_unix_to_datetime(df['date'])
df['date'] = converted_dates

symbol_list = df['crypto_id'].unique()

def plot_crypto(symbol):
    'Plot the graph given a symbol name'
    df_symbol = df[df['crypto_id'] == f'{symbol}']
    fig = go.Figure(data=go.Ohlc(x=df_symbol['date'],
                        open=df_symbol['open'],
                        high=df_symbol['high'],
                        low=df_symbol['low'],
                        close=df_symbol['close']))
    fig.update_layout(
    title=f'{symbol} currency')
    return fig.show()

#--------mplfinance: THIS WORKS-------
import mplfinance as mpl
from mpld3 import plugins
import matplotlib.pyplot as plt

mpl_df = df.set_index('date')
mpl_df.index = pd.to_datetime(mpl_df.index)

for i in range(1, len(mpl_df.columns)-2):
    mpl_df.iloc[:,i] = list(map(float, mpl_df.iloc[:,i]))

def mpl_crypto(symbol):
    "DOESN'T WORK"
    fig = plt.Figure()
    mpl.plot(mpl_df[mpl_df['crypto_id'] == f'{symbol}'])
    plugins.connect(fig)
    return mpld3.show()
