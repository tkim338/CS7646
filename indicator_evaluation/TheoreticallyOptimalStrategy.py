import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode

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
	benchmark_symbol = 'JPM'
	all_dates = date_list(sd, ed)
	stock_data = get_data([benchmark_symbol], all_dates, addSPY=False)

	buy_date = stock_data[benchmark_symbol].first_valid_index()
	sell_date = stock_data[benchmark_symbol].last_valid_index()

	# output = {'Date': [], 'Symbol': [], 'Order': [], 'Shares':[]}
	output = {'Date': [], 'Trade':[]}
	# output['Date'] = [buy_date.strftime('%Y-%m-%d'), sell_date.strftime('%Y-%m-%d')]
	output['Date'] = [buy_date, sell_date]
	# output['Symbol'] = [benchmark_symbol, benchmark_symbol]
	# output['Order'] = ['BUY', 'SELL']
	# output['Shares'] = [1000, 0]
	output['Trade'] = [1000, -1000]

	df_benchmark = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[benchmark_symbol])

	return df_benchmark

def compute(symbol, sd, ed, sv): # symbol, start date, end date, start value of portfolio
	all_dates = date_list(sd, ed)
	stock_data = get_data([symbol], all_dates, addSPY=False)
	stock_data = stock_data.fillna(method='ffill')
	stock_data = stock_data.fillna(method='bfill')
	prev_price = stock_data[symbol][all_dates[0]]
	prev_date = all_dates[0]
	current_position = 0
	# output = {'Date': [], 'Symbol': [], 'Order': [], 'Shares':[]}
	output = {'Date': [], 'Trade': []}

	for date in all_dates:
		price = stock_data[symbol][date]
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

			if prev_trade != 0:
				# output['Date'].append(prev_date.strftime('%Y-%m-%d'))
				output['Date'].append(prev_date)
				# output['Symbol'].append(symbol)
				# if prev_trade > 0:
				# 	output['Order'].append('BUY')
				# else:
				# 	output['Order'].append('SELL')
				# output['Shares'].append(np.abs(prev_trade))
				output['Trade'].append(prev_trade)

		prev_price = price
		prev_date = date

	# cover final position
	# output['Date'].append(prev_date.strftime('%Y-%m-%d'))
	output['Date'].append(prev_date)
	# output['Symbol'].append(symbol)
	# if current_position > 0:
	# 	output['Order'].append('SELL')
	# else:
	# 	output['Order'].append('BUY')
	# output['Shares'].append(np.abs(current_position))
	output['Trade'].append(-current_position)
	current_position = 0

	df_trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])

	return df_trades

def compute_statistics(port_val):
	port_val_list = port_val.values.tolist()

	daily_return = []
	prev_value = port_val[0][0]

	for pv in port_val_list:
		value = pv[0]
		daily_return.append((value - prev_value) / prev_value)
		prev_value = value

	cum_return = (port_val_list[-1][0] - port_val_list[0][0]) / port_val_list[0][0]
	stdev_daily_return = np.std(daily_return)
	mean_daily_return = np.mean(daily_return)

	return cum_return, stdev_daily_return, mean_daily_return

def testPolicy(symbol, sd, ed, sv): # symbol, start date, end date, start value of portfolio
	df_trades = compute(symbol, sd, ed, sv)
	return df_trades

if __name__ == "__main__":
	print('main code here')
	df_test = testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 1, 7), sv=100000)
	test_values = marketsimcode.compute_portvals(orders_df=df_test, start_val=100000, commission=0, impact=0)

	cum, std, mean = compute_statistics(test_values)
	print(cum)
	print(std)
	print(mean)

	print('done')