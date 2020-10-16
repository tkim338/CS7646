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

def sma(df_prices, window_size=20):
	df_sma = df_prices.rolling(window_size).mean()
	df_sma.columns = ['SMA']
	return df_sma

def bollinger_bands(df_prices, window_size=20, std_dev=2):
	df_sma = sma(df_prices, window_size)

	df_std = df_prices.rolling(window_size).std()
	df_std.columns = ['std']

	df_bb_lower = pd.DataFrame(data=df_sma['SMA'] - std_dev*df_std['std'], columns=['Bollinger Band lower band'])
	df_bb_upper = pd.DataFrame(data=df_sma['SMA'] + std_dev*df_std['std'], columns=['Bollinger Band upper band'])

	return df_bb_lower, df_bb_upper

def momentum(df_prices, window_size=5):
	def mom(x):
		return x[-1]/x[0] - 1

	df_momentum = df_prices.rolling(window_size).apply(mom)
	df_momentum.columns = ['momentum']
	return df_momentum

def volatility(df_prices, window_size=10):
	def ret(x):
		return (x[-1]-x[0])/x[0]
	df_daily_return = df_prices.rolling(2).apply(ret)

	df_volatility = df_daily_return.rolling(window_size).apply(np.std)
	df_volatility.columns = ['volatility']
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
	return df_obv

def indicator_test(symbol, sd, ed):
	all_dates = []
	day_increment = dt.timedelta(days=1)
	date_i = sd
	while date_i <= ed:
		all_dates.append(date_i)
		date_i += day_increment

	stock_price = get_data([symbol], all_dates, addSPY=False, colname='Adj Close')
	stock_price = stock_price.fillna(method='ffill')
	stock_price = stock_price.fillna(method='bfill')
	stock_price.columns = ['adj. close price']

	stock_volume = get_data([symbol], all_dates, addSPY=False, colname='Volume')
	stock_volume = stock_volume.fillna(method='ffill')
	stock_volume = stock_volume.fillna(method='bfill')

	# Technical indicators:
	# 1) SMA
	sma_window = 20
	ma = sma(stock_price, window_size=sma_window)
	ma.columns += ' ('+str(sma_window)+'-day)'
	ax_ma = stock_price.plot(title='Simple Moving Average ('+symbol+')', figsize=(10,8))
	ma.plot(ax=ax_ma)
	ax_ma.set_xlabel('Date')
	ax_ma.set_ylabel('Price ($)')
	ax_ma.grid(b=True, which='both', axis='both')
	plt.savefig('sma.png')

	# 2) Bollinger bands
	bb_window = 20
	sdev = 2
	bl, bu = bollinger_bands(stock_price, window_size=bb_window, std_dev=sdev)
	bl.columns += ' (-'+str(sdev)+' std. dev.)'
	bu.columns += ' (+'+str(sdev)+' std. dev.)'
	ax_bb = stock_price.plot(title='Bollinger Band ('+symbol+')', figsize=(10,8))
	ma.plot(ax=ax_bb)
	bu.plot(ax=ax_bb)
	bl.plot(ax=ax_bb)
	ax_bb.set_xlabel('Date')
	ax_bb.set_ylabel('Price ($)')
	ax_bb.grid(b=True, which='both', axis='both')
	plt.savefig('bollinger_band.png')

	# 3) momentum ( price[t]/price[t-N] - 1 )
	mm_window = 20
	mm = momentum(stock_price, window_size=mm_window)
	mm.columns += ' (' + str(mm_window) + '-day)'
	fig_mm, (ax1_mm, ax2_mm) = plt.subplots(2, 1, figsize=(10,8))
	stock_price.plot(title=symbol, ax=ax1_mm)
	mm.plot(ax=ax2_mm, color='r')
	ax1_mm.set_ylabel('Price ($)')
	ax2_mm.set_xlabel('Date')
	ax2_mm.set_ylabel('Index')
	ax1_mm.grid(b=True, which='both', axis='both')
	ax2_mm.grid(b=True, which='both', axis='both')
	# mm_temp = stock_price/stock_price.iloc[0,:] - 1
	# ax_mm = mm_temp.plot(title=symbol, figsize=(10,8))
	# mm.plot(ax=ax_mm, color='r')

	plt.savefig('momentum.png')

	# 4) volatility (std dev of daily returns)
	vo_window = 7
	vo = volatility(stock_price, window_size=vo_window)
	vo.columns += ' (' + str(vo_window) + '-day)'
	fig_vo, (ax1_vo, ax2_vo) = plt.subplots(2, 1, figsize=(10,8))
	stock_price.plot(title=symbol, ax=ax1_vo)
	vo.plot(ax=ax2_vo, color='r')
	ax1_vo.set_ylabel('Price ($)')
	ax2_vo.set_xlabel('Date')
	ax2_vo.set_ylabel('Index')
	ax1_vo.grid(b=True, which='both', axis='both')
	ax2_vo.grid(b=True, which='both', axis='both')
	plt.savefig('volatility.png')

	# 5) OBV (on-balance volume)
	ob_vol = obv(stock_price, stock_volume)
	fig_obv, (ax1_obv, ax2_obv) = plt.subplots(2, 1, figsize=(10,8))
	stock_price.plot(title=symbol, ax=ax1_obv)
	ob_vol.plot(ax=ax2_obv, color='r')
	ax1_obv.set_ylabel('Price ($)')
	ax2_obv.set_xlabel('Date')
	ax2_obv.set_ylabel('Index')
	ax1_obv.grid(b=True, which='both', axis='both')
	ax2_obv.grid(b=True, which='both', axis='both')
	plt.savefig('obv.png')

	# plt.show()

if __name__ == "__main__":
	start_date = dt.datetime(2008, 1, 1)
	end_date = dt.datetime(2009, 12, 31)
	sym = "JPM"

	indicator_test(sym, start_date, end_date)