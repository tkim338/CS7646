""""""  		  	   		     		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Thomas Kim (replace with your name)  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: tkim338 (replace with your User ID)  		  	   		     		  		  		    	 		 		   		 		  
GT ID: 902871961 (replace with your GT ID)  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		     		  		  		    	 		 		   		 		  
import os  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def author():
    return 'tkim338'

def compute_portvals(
    orders_file="./orders/orders.csv",  		  	   		     		  		  		    	 		 		   		 		  
    start_val=1000000,  		  	   		     		  		  		    	 		 		   		 		  
    commission=9.95,  		  	   		     		  		  		    	 		 		   		 		  
    impact=0.005,  		  	   		     		  		  		    	 		 		   		 		  
):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		     		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		     		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		     		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		     		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		     		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		     		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		     		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		     		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		     		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		     		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		  	   		     		  		  		    	 		 		   		 		  
    # TODO: Your code here

    orders_df = pd.read_csv(orders_file)

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
                    holdings['cash'] -= row['Shares'] * sym_val * (1+impact)
                else:  # sell
                    holdings[row['Symbol']] -= row['Shares']
                    holdings['cash'] += row['Shares'] * sym_val * (1-impact)
            else:
                if row['Order'] == 'BUY':
                    holdings[row['Symbol']] = row['Shares']
                    holdings['cash'] -= row['Shares'] * sym_val * (1+impact)
                else:  # sell
                    holdings[row['Symbol']] = -row['Shares']
                    holdings['cash'] += row['Shares'] * sym_val * (1-impact)
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
                pv += sym_val*holdings[key]
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

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    # start_date = dt.datetime(2008, 1, 1)
    # end_date = dt.datetime(2008, 6, 1)
    # portvals = get_data(["IBM"], pd.date_range(start_date, end_date))
    # portvals = portvals[["IBM"]]  # remove SPY
    # rv = pd.DataFrame(index=portvals.index, data=portvals.values)
    #
    # return rv
    # return portvals


    rv = pd.DataFrame(index=portvals.index, data=portvals.values)
    return rv
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def test_code():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		  	   		     		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		  	   		     		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    of = "./orders/orders.csv"
    sv = 1000000  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # Process orders  		  	   		     		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		     		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		  	   		     		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		     		  		  		    	 		 		   		 		  
    else:  		  	   		     		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # Get portfolio stats  		  	   		     		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		     		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008, 1, 1)  		  	   		     		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008, 6, 1)  		  	   		     		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		     		  		  		    	 		 		   		 		  
        0.2,  		  	   		     		  		  		    	 		 		   		 		  
        0.01,  		  	   		     		  		  		    	 		 		   		 		  
        0.02,  		  	   		     		  		  		    	 		 		   		 		  
        1.5,  		  	   		     		  		  		    	 		 		   		 		  
    ]  		  	   		     		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		     		  		  		    	 		 		   		 		  
        0.2,  		  	   		     		  		  		    	 		 		   		 		  
        0.01,  		  	   		     		  		  		    	 		 		   		 		  
        0.02,  		  	   		     		  		  		    	 		 		   		 		  
        1.5,  		  	   		     		  		  		    	 		 		   		 		  
    ]  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
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

    # of = "./orders/orders2.csv"
    # sv = 1000000
    # portvals = compute_portvals(orders_file=of, start_val=sv)
    # print(portvals[portvals.columns[0]][-1])