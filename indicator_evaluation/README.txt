testproject.py
	This file implements calls to indicators.py and TheoreticallyOptimalStrategy.py to generate all of the figures and statistics used in the report.  This file can be run as-is and should be run to produce all figures and statistics from a single entry point.

indicators.py
	This file implements indicators as functions that operate on DataFrames.  The "main" code here generates the indicator illustration figures used in the report.  The indicators implemented are: simple moving average (SMA), Bollinger Band, momentum, volatility, and on-balance volume (OBV).  This file contains a main code that runs through all indicators and produces figures for each.  This file can be run as-is.  A detailed breakdown of the indicators is below.

TheoreticallyOptimalStrategy.py
	This file implements a TheoreticallyOptimalStrategy object and testPolicy() function which returns a DataFrame containing the trades necessary to execute the optimal strategy.  This file contains a main code that calls testPolicy() using the requested stock symbol and trading dates and prints statistics required in the report (cumulative return, standard deviation of daily returns, and mean of daily returns, all for both the theoretically optimal portfolio and the benchmark.  This file also produces the figure illustrating the performance of this strategy.  This file can be run as-is.

marketsimcode.py
	This file contains code used in a previous project but modified to take in the simplified trades DataFrame used in this project.  This code returns a DataFrame with a single column containing daily returns.  This file cannot be run on its own and instead is called by other functions.


Detailed indicator function API:

SMA: df_sma = sma(df_prices, window_size=20)
Input: 
	df_prices (pandas DataFrame containing a single column of stock prices with an index based on date)
	window_size (size of rolling window used to compute mean; default is set to 20)
Output:
	df_sma (pandas DataFrame containing a single column of rolling mean of stock prices with an index based on date)


Bollinger Band: df_bb_lower, df_bb_upper = bollinger_bands(df_prices, window_size=20, std_dev=2)
Input: 
	df_prices (pandas DataFrame containing a single column of stock prices with an index based on date)
	window_size (size of rolling window used to compute mean; default is set to 20)
	std_dev (number of standard deviations separating the upper and lower Bollinger Bands from the moving average; default is set to 2)
Output:
	df_bb_lower (pandas DataFrame containing a single column of lower Bollinger Band prices with an index based on date)
	df_bb_upper (pandas DataFrame containing a single column of upper Bollinger Band prices with an index based on date)


momentum: df_momentum = momentum(df_prices, window_size=5)
Input:
	df_prices (pandas DataFrame containing a single column of stock prices with an index based on date)
	window_size (size of rolling window used to compute momentum; default is set to 5)
Output:
	df_momentum (pandas DataFrame containing a single column of momentum value with an index based on date)


volatility: df_volatility = volatility(df_prices, window_size=10)
Input:
	df_prices (pandas DataFrame containing a single column of stock prices with an index based on date)
	window_size (size of rolling window used to compute volatility; default is set to 10)
Output:
	df_volatility (pandas DataFrame containing a single column of volatility value with an index based on date)


on-balance volume: df_obv = obv(df_prices, df_volume)
Input:
	df_prices (pandas DataFrame containing a single column of stock prices with an index based on date)
	df_volume (pandas DataFrame containing a single column of trade volume with an index based on date)
Output:
	df_obv (pandas DataFrame containing a single column of OBV value with an index based on date)



