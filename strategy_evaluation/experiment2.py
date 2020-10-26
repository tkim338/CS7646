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

	output_df_list = []
	impacts = [0, 0.005, 0.01, 0.1]
	for imp in impacts:
		learner = sl.StrategyLearner()
		learner.add_evidence(symbol=sym, sd=start_date, ed=end_date)
		trades_sl = learner.testPolicy(symbol=sym, sd=start_date, ed=end_date, sv=100000)
		vals_sl = msc.compute_portvals(trades_sl, start_val=100000, commission=0, impact=imp)
		vals_sl = vals_sl / vals_sl[0][0]
		vals_sl.columns = ['impact: '+str(imp)]
		output_df_list.append(vals_sl)

	trades_bm = benchmark()
	vals_bm = msc.compute_portvals(trades_bm, start_val=100000, commission=9.95, impact=0.005)
	vals_bm = vals_bm / vals_bm[0][0]
	vals_bm.columns = ['benchmark']

	output = pd.DataFrame([vals_bm['benchmark'], output_df_list[0]['impact: '+str(impacts[0])], output_df_list[1]['impact: '+str(impacts[1])], output_df_list[2]['impact: '+str(impacts[2])], output_df_list[3]['impact: '+str(impacts[3])]]).transpose()
	output = output.fillna(method='ffill')
	output = output.fillna(method='bfill')
	output_plot = output.plot()
	output_plot.set_xlabel('Date')
	output_plot.set_ylabel('Normalized Value')
	output_plot.grid(b=True, which='both', axis='both')
	plt.savefig('experiment2.png')
	# plt.show()

if __name__ == "__main__":
	run()