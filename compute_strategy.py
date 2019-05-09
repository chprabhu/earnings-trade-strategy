import pandas as pd
import numpy as np
from constants import *


def get_pre_earnings_trading_returns(ticker):
	'''
	This function returns a list of return rates, assuming that we buy at the open 'num_days' 
	before the earnings announce date, and sell near the close of the earnings announce date

	BTO = Before Trading Opens
	DMT = During Market Trading
	AMC = After Market Close
	'''
	
	return_rates = []

	try:
		price_data = pd.read_csv(stock_price_data_path + ticker + ".csv", parse_dates=['timestamp'])
		earnings = earnings_dates[earnings_dates['ticker'] == ticker]
	except:
		print(ticker + " Error reading in price data")
		error_tickers.append(ticker)
		return return_rates	

	for row in earnings.itertuples():
		earnings_date = row[2] # get back earnings date
		announce_time = row[3] # get back announce time
		try:
			if (announce_time == "BTO" or announce_time == "DMT"):
				# get data from num_days+1 trading days ago up to 1 trading day ago
				begin_index = price_data[price_data['timestamp'] == earnings_date].index.values[0] + 1
			elif (announce_time == "AMC"):
				# get data from num_days trading days ago up to today
				begin_index = price_data[price_data['timestamp'] == earnings_date].index.values[0]
			else:
				print('Invalid Announce Time Code: ' + ticker)
				continue

			end_index = begin_index + num_days
			window = price_data[begin_index:end_index]
			return_rate = (window['close'][begin_index] / window['open'][end_index-1]) - 1
			return_rates.append(return_rate)
		except (IndexError, ValueError) as error:
			print(ticker + " Error pulling price data subset")
			error_tickers.append(ticker)
			break

	return return_rates


def get_returns_table(tickers):
	'''
	This function returns a table that has the following columns:
	
	Ticker - Ticker symbol
	R1-R5  - Stock return for specified time period. R1 uses the most recent earnings date,
			 with each subsequent R going backwards in time
	'''

	returns_table = pd.DataFrame(columns=['R1', 'R2', 'R3', 'R4', 'R5'])

	for i, ticker in enumerate(tickers):
		get_returns = get_pre_earnings_trading_returns(ticker)

		# Some stocks don't have 5 earnings dates. Append zeros until length equals 5
		while len(get_returns) < 5:
			get_returns.append(0)
	    
		get_returns = pd.Series(get_returns, index=['R1', 'R2', 'R3', 'R4', 'R5'])
		returns_table = returns_table.append(get_returns, ignore_index=True)
		print(str(i) + ": " + ticker + " - Complete")

	returns_table.index = tickers
	return returns_table

if __name__ == '__main__':
	error_tickers = []

	earnings_dates = pd.read_csv(earnings_dates_data_path + "earnings_dates.csv", parse_dates=["earnings_date"])
	tickers = list(earnings_dates['ticker'].unique())
	
	returns_table = get_returns_table(tickers)
	print(returns_table)
	print(error_tickers)
	returns_table.to_csv(earnings_dates_data_path + "returns_table.csv", index_label = 'ticker')
