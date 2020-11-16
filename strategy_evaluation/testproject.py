import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc
import pandas as pd
from util import get_data
import matplotlib.pyplot as plt
import datetime as dt
import experiment1
import experiment2

def author():
	return 'tkim338'

if __name__ == "__main__":
	# experiment1.run()
	# experiment2.run()
	man = ms.ManualStrategy()
	in_test = man.in_sample_test()
	out_test = man.out_sample_test()

	in_test_val = in_test.values
	out_test_val = out_test.values
	plt.clf()
	plt.figure(figsize=(15,8))
	plt.plot(in_test_val)
	plt.plot(out_test_val)
	plt.legend(['In-sample performance', 'Out-of-sample performance'])
	plt.xlabel('Time from start [day]')
	plt.ylabel('Normalized Value (relative to benchmark)')
	plt.savefig('in_out_comparison.png')