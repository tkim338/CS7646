import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc
import pandas as pd
from util import get_data
import matplotlib.pyplot as plt
import datetime as dt

def author():
	return 'tkim338'

def benchmark(benchmark_symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
	stock_data = get_data([benchmark_symbol], pd.date_range(sd, ed), addSPY=False)

	buy_date = stock_data[benchmark_symbol].first_valid_index()
	sell_date = stock_data[benchmark_symbol].last_valid_index()

	output = {'Date': [], 'Trade':[]}
	output['Date'] = [buy_date, sell_date]
	output['Trade'] = [1000, -1000]

	df_benchmark = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[benchmark_symbol])

	return df_benchmark

def run():
	sym = 'JPM'
	start_date = dt.datetime(2008, 1, 1)
	end_date = dt.datetime(2009, 12, 31)

	man = ms.ManualStrategy()
	trades_man = man.testPolicy(symbol=sym, sd=start_date, ed=end_date)
	vals_man = msc.compute_portvals(trades_man, start_val=100000, commission=9.95, impact=0.005)
	vals_man = vals_man / vals_man[0][0]
	vals_man.columns = ['manual strategy']

	learner = sl.StrategyLearner()
	learner.add_evidence(symbol=sym, sd=start_date, ed=end_date)
	trades_sl = learner.testPolicy(symbol=sym, sd=start_date, ed=end_date, sv=100000)
	vals_sl = msc.compute_portvals(trades_sl, start_val=100000, commission=9.95, impact=0.005)
	vals_sl = vals_sl / vals_sl[0][0]
	vals_sl.columns = ['strategy learner']

	trades_bm = benchmark()
	vals_bm = msc.compute_portvals(trades_bm, start_val=100000, commission=9.95, impact=0.005)
	vals_bm = vals_bm / vals_bm[0][0]
	vals_bm.columns = ['benchmark']

	output = pd.DataFrame([vals_bm['benchmark'], vals_man['manual strategy'], vals_sl['strategy learner']]).transpose()
	output = output.fillna(method='ffill')
	output = output.fillna(method='bfill')
	output_plot = output.plot(figsize=(10,8))
	output_plot.set_xlabel('Date')
	output_plot.set_ylabel('Normalized Value')
	output_plot.grid(b=True, which='both', axis='both')
	plt.savefig('experiment1.png')
	# plt.show()

if __name__ == "__main__":
	run()