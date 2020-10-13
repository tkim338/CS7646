import pandas as pd
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt
import numpy as np

def author():
	return 'tkim338'

# Technical indicators:
# 1) SMA
# 2) Bollinger bands
# 3) momentum ( price[t]/price[t-N] - 1 )
# 4) volatility (std dev of daily returns)
# 5) ROC (price rate of change)

def sma(df_prices, window_size=20):
	df_sma = df_prices.rolling(window_size).mean()
	df_sma.columns = ['SMA']
	return df_sma

def bollinger_bands(df_prices, window_size=20):
	df_sma = sma(df_prices, window_size)

	df_std = df_prices.rolling(window_size).std()
	df_std.columns = ['std']

	df_bb_lower = pd.DataFrame(data=df_sma['SMA'] - 2*df_std['std'], columns=['Bollinger Band lower bound'])
	df_bb_upper = pd.DataFrame(data=df_sma['SMA'] + 2*df_std['std'], columns=['Bollinger Band upper bound'])

	return df_bb_lower, df_bb_upper

def momentum(df_prices, window_size=5):
	def mom(x):
		return x[-1]/x[0] - 1

	df_momentum = df_prices.rolling(window_size).apply(mom)
	df_momentum.columns = ['momentum']
	return df_momentum

def volatility(df_prices, window_size=20):
	df_volatility = df_prices.rolling(window_size).apply(np.var)
	df_volatility.columns = ['volatility']
	return df_volatility

def roc(df_prices, window_size=10):
	def r(x):
		return 100 * (x[-1]-x[0])/x[0]

	df_roc = df_prices.rolling(window_size).apply(r)
	df_roc.columns = ['ROC']
	return df_roc

if __name__ == "__main__":
	print('main code here')

	symbol = "AAPL"
	sd = dt.datetime(2009, 1, 1)
	ed = dt.datetime(2010, 1, 7)

	all_dates = []
	day_increment = dt.timedelta(days=1)
	date_i = sd
	while date_i <= ed:
		all_dates.append(date_i)
		date_i += day_increment

	stock_data = get_data([symbol], all_dates, addSPY=False)
	stock_data = stock_data.fillna(method='ffill')
	stock_data = stock_data.fillna(method='bfill')

	ma = sma(stock_data)
	bl, bu = bollinger_bands(stock_data)
	mm = momentum(stock_data)
	vo = volatility(stock_data)
	ro = roc(stock_data)

	figure = stock_data.plot(title=symbol)
	ma.plot(ax=figure)
	bl.plot(ax=figure)
	bu.plot(ax=figure)
	mm.plot()
	vo.plot()
	ro.plot()
	plt.show()
