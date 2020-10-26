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
	# experiment2.run()