import datetime as dt
import os  		  	   		     		  		  		    	 		 		   		 		  
import random  		  	   		     		  		  		    	 		 		   		 		  
import sys  		  	   		     		  		  		    	 		 		   		 		  
import time  		  	   		     		  		  		    	 		 		   		 		  
import traceback as tb  		  	   		     		  		  		    	 		 		   		 		  
from collections import namedtuple
import numpy as np
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
import pytest  		  	   		     		  		  		    	 		 		   		 		  
import util
import StrategyLearner

description = "AAPL"
insample_args = dict(
    symbol="AAPL",
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 12, 31),
    sv=100000,
)
outsample_args = dict(
    symbol="AAPL",
    sd=dt.datetime(2010, 1, 1),
    ed=dt.datetime(2011, 12, 31),
    sv=100000,
)
benchmark_type = "stock"
benchmark = 0.1581999999999999  # benchmark computed Nov 22 2017
impact = 0.0
seed = 1481090000

np.random.seed(seed)
random.seed(seed)

learner = StrategyLearner.StrategyLearner(verbose=False, impact=impact)

learner.add_evidence(**insample_args)

insample_trades_1 = learner.testPolicy(**insample_args)

insample_trades_2 = learner.testPolicy(**insample_args)

outsample_trades = learner.testPolicy(**outsample_args)

print()