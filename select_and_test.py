import pandas as pd
import numpy as np
from constants import *


if __name__ == "__main__": 
	earnings_tbl = pd.read_csv(earnings_dates_data_path + "returns_table.csv", index_col=['ticker'])
	sum_series = (earnings_tbl[['R2', 'R3', 'R4', 'R5']] > 0).sum(axis=1)

	focus_tickers = sum_series[sum_series == 4]
	avg_return = earnings_tbl.loc[list(focus_tickers.index.values)]['R1'].mean()
	print("Four in a row: " + str(avg_return))

	focus_tickers = sum_series[sum_series >= 3]
	avg_return = earnings_tbl.loc[list(focus_tickers.index.values)]['R1'].mean()
	print("Three out of Four, or Four in a row: " + str(avg_return))


