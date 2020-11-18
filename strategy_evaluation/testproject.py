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
	experiment1.run()
	experiment2.run()
	man = ms.ManualStrategy()
	in_test, in_ret_bm, in_ret_man = man.in_sample_test()
	out_test, out_ret_bm, out_ret_man = man.out_sample_test()

	print(['In-sample, benchmark cumulative return: ', in_ret_bm[0]])
	print(['In-sample, benchmark mean daily return: ', in_ret_bm[1]])
	print(['In-sample, benchmark std. dev. of daily return: ', in_ret_bm[2]])
	print('')
	print(['In-sample, manual strategy cumulative return: ', in_ret_man[0]])
	print(['In-sample, manual strategy mean daily return: ', in_ret_man[1]])
	print(['In-sample, manual strategy std. dev. of daily return: ', in_ret_man[2]])
	print('')
	print(['Out-of-sample, benchmark cumulative return: ', out_ret_bm[0]])
	print(['Out-of-sample, benchmark mean daily return: ', out_ret_bm[1]])
	print(['Out-of-sample, benchmark std. dev. of daily return: ', out_ret_bm[2]])
	print('')
	print(['Out-of-sample, manual strategy cumulative return: ', out_ret_man[0]])
	print(['Out-of-sample, manual strategy mean daily return: ', out_ret_man[1]])
	print(['Out-of-sample, manual strategy std. dev. of daily return: ', out_ret_man[2]])

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