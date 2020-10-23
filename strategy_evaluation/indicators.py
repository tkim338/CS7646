import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author():
	return 'tkim338'

# Technical indicators:
# 1) SMA
# 2) Bollinger bands
# 3) momentum ( price[t]/price[t-N] - 1 )
# 4) volatility (std dev of daily returns)
# 5) OBV (on-balance volume)

def normalize(df_data):
	# base_val = None
	# for r in df_data.iterrows():
	# 	if not np.isnan(r[1][0]) and r[1][0] != 0:
	# 		base_val = r[1][0]
	# 		break
	# df_data = df_data / base_val
	# return df_data

	df_data = (df_data - np.mean(df_data)) / np.std(df_data)
	return df_data

def sma(df_prices, window_size=20):
	df_sma = df_prices.rolling(window_size).mean()
	df_sma.columns = ['SMA']
	# df_sma = normalize(df_sma)
	return df_sma

def bollinger_bands(df_prices, window_size=20, std_dev=2):
	df_sma = sma(df_prices, window_size)

	df_std = df_prices.rolling(window_size).std()
	df_std.columns = ['std']

	df_bb_lower = pd.DataFrame(data=df_sma['SMA'] - std_dev*df_std['std'], columns=['bb_lower'])
	df_bb_upper = pd.DataFrame(data=df_sma['SMA'] + std_dev*df_std['std'], columns=['bb_upper'])

	return df_bb_lower, df_bb_upper

def momentum(df_prices, window_size=5):
	def mom(x):
		return x[-1]/x[0] - 1

	df_momentum = df_prices.rolling(window_size).apply(mom)
	df_momentum.columns = ['momentum']
	df_momentum = normalize(df_momentum)
	return df_momentum

def volatility(df_prices, window_size=10):
	def ret(x):
		return (x[-1]-x[0])/x[0]
	df_daily_return = df_prices.rolling(2).apply(ret)

	df_volatility = df_daily_return.rolling(window_size).apply(np.std)
	df_volatility.columns = ['volatility']
	df_volatility = normalize(df_volatility)
	return df_volatility

def obv(df_prices, df_volume):
	df_data = pd.concat([df_prices, df_volume], axis=1, sort=False)
	df_data.columns = ['price', 'volume']

	obv_list = {'date': [], 'obv':[]}
	prev_price = df_data['price'][0]
	prev_obv = 0
	for d in df_data.iterrows():
		obv_list['date'].append(d[0])
		curr_price = d[1]['price']
		if curr_price > prev_price:
			obv_list['obv'].append(prev_obv + d[1]['volume'])
		elif curr_price < prev_price:
			obv_list['obv'].append(prev_obv - d[1]['volume'])
		else:
			obv_list['obv'].append(prev_obv)
		prev_price = curr_price
		prev_obv = obv_list['obv'][-1]
	df_obv = pd.DataFrame(data=obv_list['obv'], index=obv_list['date'], columns=['OBV'])
	df_obv = normalize(df_obv)
	return df_obv