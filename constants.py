## If you are going to run this, please use your own tokens and API keys
## Note, it costs money to pull data from IEX

os.environ["IEX_API_VERSION"] = "iexcloud-beta"
os.environ["IEX_TOKEN"] = "{token}"

stock_price_data_path = "stock_returns/"
earnings_dates_data_path = "stock_returns/earnings_dates/"
apikey = "{token}"
num_days = 5


