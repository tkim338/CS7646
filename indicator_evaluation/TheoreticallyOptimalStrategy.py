import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
import marketsimcode
import matplotlib.pyplot as plt

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

	output = {'Date': [], 'Trade':[]}
	output['Date'] = [buy_date, sell_date]
	output['Trade'] = [1000, -1000]

	df_benchmark = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[benchmark_symbol])

	return df_benchmark

def compute(symbol, sd, ed, sv): # symbol, start date, end date, start value of portfolio
	all_dates = date_list(sd, ed)
	stock_data = get_data([symbol], all_dates, addSPY=False)
	prev_price = stock_data[symbol][all_dates[0]]
	prev_date = all_dates[0]
	current_position = 0
	output = {'Date': [], 'Trade': []}

	for date in all_dates:
		price = stock_data[symbol][date]
		if not np.isnan(price):
			delta = price - prev_price
			prev_trade = 0
			if delta > 0:
				if current_position != 1000:
					prev_trade = 1000 - current_position
					current_position = 1000
				else:
					prev_trade = 0
					current_position = 1000
			elif delta < 0:
				if current_position != -1000:
					prev_trade = -1000 - current_position
					current_position = -1000
				else:
					prev_trade = 0
					current_position = -1000

			if prev_trade != 0:
				output['Date'].append(prev_date)
				output['Trade'].append(prev_trade)

			prev_price = price
			prev_date = date

	# cover final position
	output['Date'].append(prev_date)
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

def generateReport(symbol, sd, ed):
	df_trades = testPolicy(symbol, sd, ed, 100000)
	tos_values = marketsimcode.compute_portvals(orders_df=df_trades, start_val=100000, commission=0, impact=0)
	cum, std, mean = compute_statistics(tos_values)

	bm_df = benchmark(sd, ed, 100000)
	bm_values = marketsimcode.compute_portvals(orders_df=bm_df, start_val=100000, commission=0, impact=0)
	bm_cum, bm_std, bm_mean = compute_statistics(bm_values)

	df_temp = pd.concat([tos_values / tos_values.iloc[0, :], bm_values / bm_values.iloc[0, :]], axis=1, sort=False)
	df_temp.columns = ['theoretically optimal portfolio', 'benchmark']

	# -Benchmark (see definition above) normalized to 1.0 at the start: Green line
	# -Value of the theoretically optimal portfolio (normalized to 1.0 at the start): Red line
	val_plot = df_temp.plot(style=['-r', '-g'], title='Theoretically Optimal Portfolio versus benchmark (' + symbol + ')', figsize=(10, 8))
	val_plot.set_xlabel('Date')
	val_plot.set_ylabel('Normalized Value')
	val_plot.grid(b=True, which='both', axis='both')
	plt.savefig('TOS.png')

	print('Symbol: ', symbol)
	print('Start date: ', sd)
	print('End date: ', ed)
	# -Cumulative return of the benchmark and portfolio
	print('Cumulative return of the benchmark: ', bm_cum, ' and portfolio: ', cum)
	# -Stdev of daily returns of benchmark and portfolio
	print('Stdev of daily returns of benchmark: ', bm_std, ' and portfolio: ', std)
	# -Mean of daily returns of benchmark and portfolio
	print('Mean of daily returns of benchmark: ', bm_mean, ' and portfolio: ', mean)

if __name__ == "__main__":
	# df_test = testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
	# test_values = marketsimcode.compute_portvals(orders_df=df_test, start_val=100000, commission=0, impact=0)
	# # stock_data = get_data(['JPM'], date_list(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31)), addSPY=False)
	#
	# # df_test.columns = ['trades']
	# # stock_data.columns = ['price']
	# # df_temp = pd.concat([df_test, stock_data], axis=1, sort=False)
	#
	# cum, std, mean = compute_statistics(test_values)
	# print(cum)
	# print(std)
	# print(mean)
	#
	# print('done')
	generateReport(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))