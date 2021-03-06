# earnings-trade-strategy
Trading Strategy Test

## Hypothesis
Stocks that tend to trade up in the few days right before they release their earnings will consistently do so. A profitable trading strategy might be to buy at the open a few days before the earnings release, and sell at the close right before the day of the earnings release

## Files
- `constants.py` contains variables that you may want to adjust, as well as any API keys required to download the data
- `download_data_to_csv.py` allows you to download historical price data and historic earnings release dates for all 500 stocks in the S&P 500
- `compute_strategy.py` returns a table of returns for the window defined by num_days in `constants.py` before an earnings release for each stock in the S&P 500
- `select_and_test.py` Identifies a basket of stocks that tends to trade up before earnings. Test the strategy by assuming you would have bought and sold that stock in the most recent earnings release pre-window.

## Order of Execution
1. Update any necessary variables in `constants.py`
2. Run `download_data_to_csv.py` if you don't have the data. Note that downloading the price data takes a very long time, and downloading the earnings dates will cost about $3 in API call fees
3. Run `compute_strategy.py`
4. Run `select_and_test.py`
