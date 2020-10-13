import datetime as dt
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data

def author():
	return 'tkim338'

def compute_portvals(
		orders_df,
		start_val=1000000,
		commission=9.95,
		impact=0.005
):

	# orders_df = pd.read_csv(orders_file)

	start_date = dt.datetime.strptime(orders_df["Date"].min(), '%Y-%m-%d')
	end_date = dt.datetime.strptime(orders_df["Date"].max(), '%Y-%m-%d')
	day_increment = dt.timedelta(days=1)
	all_dates = []
	date_i = start_date
	while date_i <= end_date:
		all_dates.append(date_i)
		date_i += day_increment

	portvals = get_data(['$SPX'], pd.date_range(start_date, end_date), addSPY=False)
	holdings = {'cash': start_val}

	retrieved_data = {}

	def update_holdings(date):
		curr_orders = orders_df.loc[orders_df['Date'] == date.strftime('%Y-%m-%d')]
		for index, row in curr_orders.iterrows():
			sym_val = get_data([row['Symbol']], [date], addSPY=False)[row['Symbol']].iloc[0]
			holdings['cash'] -= commission

			if row['Symbol'] in holdings:
				if row['Order'] == 'BUY':
					holdings[row['Symbol']] += row['Shares']
					holdings['cash'] -= row['Shares'] * sym_val * (1 + impact)
				else:  # sell
					holdings[row['Symbol']] -= row['Shares']
					holdings['cash'] += row['Shares'] * sym_val * (1 - impact)
			else:
				if row['Order'] == 'BUY':
					holdings[row['Symbol']] = row['Shares']
					holdings['cash'] -= row['Shares'] * sym_val * (1 + impact)
				else:  # sell
					holdings[row['Symbol']] = -row['Shares']
					holdings['cash'] += row['Shares'] * sym_val * (1 - impact)
		return holdings

	def get_portfolio_value(curr_holdings, date):
		pv = 0
		for key in holdings:
			if key == 'cash':
				pv += curr_holdings[key]
			else:
				if key not in retrieved_data:
					retrieved_data[key] = get_data([key], all_dates, addSPY=False)
				sym_val = retrieved_data[key][key][date]
				pv += sym_val * holdings[key]
		return pv

	curr_date = start_date

	while curr_date <= end_date:
		spx_df = get_data(['$SPX'], [curr_date], addSPY=False)
		if not np.isnan(spx_df['$SPX'].iloc[0]):
			# update holdings based on today's orders
			holdings = update_holdings(curr_date)

			# compute today's portfolio value
			curr_pv = get_portfolio_value(holdings, curr_date)

			# update portfolio value with today's value
			portvals['$SPX'][curr_date] = curr_pv
		else:
			portvals = portvals.drop(curr_date)

		# go to next trading day
		curr_date += day_increment

	rv = pd.DataFrame(index=portvals.index, data=portvals.values)
	return rv

if __name__ == "__main__":
	# test_code()

	# symbols = ["AAPL"]
	# dates = [dt.datetime(2011, 1, 10), dt.datetime(2012, 1, 10), ]
	# dat = get_data(symbols, dates)
	# print(dat)

	# d1 = dt.datetime(2012, 1, 1)
	# d2 = d1 + dt.timedelta(days=1)
	#
	# print(d1)
	# print(d2)

	# df = get_data(['$SPX'], [dt.datetime(2012, 8, 27), dt.datetime(2012, 8, 24), dt.datetime(2012, 8, 25)], addSPY=False)
	# print(df)

	of = "../marketsim/orders/orders2.csv"
	sv = 1000000
	portvals = compute_portvals(orders_df=pd.read_csv(of), start_val=sv)
	print(portvals[portvals.columns[0]][-1])