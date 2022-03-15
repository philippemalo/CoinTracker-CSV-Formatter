import pandas as pd
from datetime import datetime as dt

ftx_trades = pd.read_csv('FTX_trades_2021.csv')

cointracker_template = pd.read_csv('cointracker_csv_import_v4.csv')

print(ftx_trades.head())
print(cointracker_template.head())

def reformatPerpTrades(ftxTrade):
    if '-' in ftxTrade.Market:
        ftxTrade.Market = ftxTrade.Market.replace('-', '/')
    if 'PERP' in ftxTrade.Market:
        ftxTrade.Market = ftxTrade.Market.replace('PERP', 'USD')
    return ftxTrade

formattedTrades = ftx_trades.apply(reformatPerpTrades, axis=1)

def ftxToCointrackerFormat(ftxTrade):
    if ":" == ftxTrade.Time[-3:-2]:
        ftxTrade.Time = ftxTrade.Time[:-3]+ftxTrade.Time[-2:]
    date = dt.strptime(ftxTrade.Time, '%Y-%m-%dT%H:%M:%S.%f%z')
    convertedDate = date.strftime('%m/%d/%Y %H:%M:%S')

    receivedCurrency = ''
    sentCurrency = ''
    if ftxTrade.Side == 'buy':
        receivedCurrency = ftxTrade.Market.split('/')[0]
        sentCurrency = ftxTrade.Market.split('/')[1]
    elif ftxTrade.Side == 'sell':
        receivedCurrency = ftxTrade.Market.split('/')[1]
        sentCurrency = ftxTrade.Market.split('/')[0]

    receivedQuantity = 0
    sentQuantity = 0
    if ftxTrade.Side == 'buy':
        receivedQuantity = ftxTrade.Size
        sentQuantity = ftxTrade.Total
    elif ftxTrade.Side == 'sell':
        receivedQuantity = ftxTrade.Total
        sentQuantity = ftxTrade.Size

    feeAmmount = ftxTrade.Fee
    feeCurrency = ftxTrade['Fee Currency']

    return convertedDate, round(receivedQuantity, 8), receivedCurrency, round(sentQuantity, 8), sentCurrency, round(feeAmmount, 8), feeCurrency

coinTrackerData = cointracker_template.iloc[0:0]

for index, trade in formattedTrades.iterrows():
    date, receivedQuantity, receivedCurrency, sentQuantity, sentCurrency, feeAmmount, feeCurrency = ftxToCointrackerFormat(trade)
    d = {"Date": date, "Received Quantity": receivedQuantity, "Received Currency": receivedCurrency, "Sent Quantity": sentQuantity, "Sent Currency": sentCurrency, "Fee Amount": feeAmmount, "Fee Currency": feeCurrency, "Tag": ""}
    coinTrackerData = coinTrackerData.append(d, ignore_index=True)

print(coinTrackerData.head())

coinTrackerData.to_csv('FtxTradesFormattedForCoinTracker.csv', index=False)