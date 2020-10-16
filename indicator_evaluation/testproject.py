import pandas as pd
import datetime as dt
from util import get_data, plot_data
import matplotlib.pyplot as plt
import numpy as np
import indicators
import TheoreticallyOptimalStrategy as tos
import marketsimcode

if __name__ == "__main__":
	start_date = dt.datetime(2008, 1, 1)
	end_date = dt.datetime(2009, 12, 31)
	sym = "JPM"

	df_trades = tos.testPolicy(symbol=sym, sd=start_date, ed=end_date, sv=100000)
	tos_values = marketsimcode.compute_portvals(orders_df=df_trades, start_val=100000, commission=0, impact=0)
	cum, std, mean = tos.compute_statistics(tos_values)

	bm_df = tos.benchmark(sd=start_date, ed=end_date, sv=100000)
	bm_values = marketsimcode.compute_portvals(orders_df=bm_df, start_val=100000, commission=0, impact=0)
	bm_cum, bm_std, bm_mean = tos.compute_statistics(bm_values)

	# df_temp = pd.concat([pd.DataFrame(data=values/values[0], index=df.index.values), pd.DataFrame(data=bm_values/bm_values[0], index=df.index.values)], axis=1, sort=False)
	df_temp = pd.concat([tos_values/tos_values.iloc[0,:], bm_values/bm_values.iloc[0,:]], axis=1, sort=False)
	df_temp.columns = ['theoretically optimal portfolio', 'benchmark']

	# -Benchmark (see definition above) normalized to 1.0 at the start: Green line
	# -Value of the theoretically optimal portfolio (normalized to 1.0 at the start): Red line
	val_plot = df_temp.plot(style=['-r', '-g'], title='Theoretically Optimal Portfolio versus benchmark ('+sym+')', figsize=(10,8))
	val_plot.set_xlabel('Date')
	val_plot.set_ylabel('Normalized Value')
	plt.savefig('TOS.png')
	# plt.show()
	# -Cumulative return of the benchmark and portfolio
	print('Cumulative return of the benchmark: ', bm_cum,' and portfolio: ', cum)
	# -Stdev of daily returns of benchmark and portfolio
	print('Stdev of daily returns of benchmark: ', bm_std,' and portfolio: ', std)
	# -Mean of daily returns of benchmark and portfolio
	print('Mean of daily returns of benchmark: ', bm_mean, ' and portfolio: ', mean)

	indicators.indicator_test(sym, start_date, end_date)