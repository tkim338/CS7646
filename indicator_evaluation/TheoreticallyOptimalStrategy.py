import datetime as dt
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data

def author():
	return 'tkim338'

def date_list(sd, ed):
	all_dates = []
	day_increment = dt.timedelta(days=1)
	date_i = sd
	while date_i <= ed:
		all_dates.append(date_i)
		date_i += day_increment
	return all_dates

def benchmark(sd, ed, sv=100000):
	all_dates = date_list(sd, ed)
	stock_data = get_data(['JPM'], all_dates, addSPY=False)
	stock_data = stock_data.fillna(method='ffill')
	stock_data = stock_data.fillna(method='bfill')

	output = {'date': [], 'value': []}
	daily_return = []
	prev_value = sv
	new_value = sv
	prev_price = stock_data['JPM'][all_dates[0]]
	for date in all_dates:
		price = stock_data['JPM'][date]
		delta = price - prev_price
		output['date'].append(date)
		new_value += delta * 1000
		output['value'].append(new_value)
		daily_return.append((new_value - prev_value) / prev_value)
		prev_value = new_value
		prev_price = price

	df_benchmark = pd.DataFrame(data=output, index=output['date'], columns=['value'])

	cum_return = (new_value - sv) / sv
	stdev_daily_return = np.std(daily_return)
	mean_daily_return = np.mean(daily_return)

	return df_benchmark, cum_return, stdev_daily_return, mean_daily_return, output['value']

def compute(symbol, sd, ed, sv): # symbol, start date, end date, start value of portfolio
	all_dates = date_list(sd, ed)
	stock_data = get_data([symbol], all_dates, addSPY=False)
	stock_data = stock_data.fillna(method='ffill')
	stock_data = stock_data.fillna(method='bfill')

	prev_price = stock_data[symbol][all_dates[0]]
	prev_date = all_dates[0]
	current_position = 0
	output = {'date': [], 'trades':[]}
	daily_return = []
	prev_value = sv
	new_value = sv
	values = [sv]
	for date in all_dates:
		price = stock_data[symbol][date]
		delta = 0
		if prev_price and not np.isnan(price):
			delta = price - prev_price
			if delta > 0:
				prev_trade = 1000 - current_position
				current_position = 1000
			elif delta < 0:
				prev_trade = -1000 - current_position
				current_position = -1000
			else:
				prev_trade = 0 - current_position
				current_position = 0

			output['date'].append(prev_date)
			output['trades'].append(prev_trade)

		new_value += np.abs(delta) * 1000
		values.append(new_value)
		daily_return.append((new_value - prev_value) / prev_value)
		prev_value = new_value
		prev_price = price
		prev_date = date

	# neutral final position
	output['date'].append(prev_date)
	output['trades'].append(0 - current_position)
	current_position = 0

	cum_return = (new_value - sv) / sv
	stdev_daily_return = np.std(daily_return)
	mean_daily_return = np.mean(daily_return)

	df_trades = pd.DataFrame(data=output, index=output['date'], columns=['trades'])

	return df_trades, cum_return, stdev_daily_return, mean_daily_return, values

def testPolicy(symbol, sd, ed, sv): # symbol, start date, end date, start value of portfolio
	df_trades = compute(symbol, sd, ed, sv)
	return df_trades

if __name__ == "__main__":
	print('main code here')
	#testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv=100000)
	testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 1, 7), sv=100000)

	df, cum, std, mean, values = compute(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 1, 7), sv=100000)
	# df, cum, std, mean, values = benchmark(sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 1, 7), sv=100000)
	print(cum)
	print(std)
	print(mean)

	print('done')