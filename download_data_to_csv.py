import pandas as pd
import numpy as np
import bs4 as bs
import pickle
import os
import requests

from datetime import timedelta
from pandas.tseries.offsets import BDay
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from constants import *


def save_sp500_tickers():
	resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', {'class': 'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		ticker = ticker.strip('\n')
		tickers.append(ticker)
        
	with open("sp500tickers.pickle","wb") as f:
		pickle.dump(tickers,f)
        
	return tickers


def get_stock_earnings_table(ticker):
	stock = Stock(ticker, output_format='pandas')
	stock_earnings = stock.get_earnings(last=5)
	return stock_earnings


def create_earnings_dates_csv(tickers):
	earnings_df = pd.DataFrame({"ticker":[], "earnings_date":[], "announce_time":[]})

	for i, ticker in enumerate(tickers):
		earnings_table = get_stock_earnings_table(ticker)
		earnings_dates = list(earnings_table.index)
		announce_time = list(earnings_table['announceTime'].values)
		ticker_list = [ticker] * len(earnings_dates)
		temp_df = pd.DataFrame({"ticker":ticker_list, "earnings_date":earnings_dates, "announce_time":announce_time})
		earnings_df = earnings_df.append(temp_df, ignore_index=True)
		print(str(i) + " : " + ticker)

	earnings_df.to_csv(earnings_dates_data_path + "earnings_dates.csv", index=False)

def create_stock_price_data_csv(tickers):
	for i, ticker in enumerate(tickers):
		print("Pulling data for " + ticker)
		CSV_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&outputsize=full&datatype=csv&apikey=" + apikey
		temp_df = pd.read_csv(CSV_URL)
		if temp_df.shape[0] == 2:
			print("Sleeping for 90 seconds...")
			time.sleep(90)
			temp_df = pd.read_csv(CSV_URL)
	temp_df.to_csv(stock_price_data_path + ticker + ".csv", index=False)
	print(temp_df.shape)


if __name__ == '__main__':
	tickers = save_sp500_tickers()
	
	# If you want to create a fresh earnings dates file, uncomment the next line of code
	# and uncomment the IEX os variables in the constants.py file
	# Otherwise, grab the earnings_dates.csv file in the repo and put it in the earnings_dates_data_path folder

	#create_earnings_dates_csv(tickers)

	create_stock_price_data_csv(tickers)
