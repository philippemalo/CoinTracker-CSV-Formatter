import pandas as pd

ftx_trades = pd.read_csv('FtxTradesFormattedForCoinTracker.csv')

print(ftx_trades.head())
print(ftx_trades["Received Currency"].unique())
print(ftx_trades["Sent Currency"].unique())