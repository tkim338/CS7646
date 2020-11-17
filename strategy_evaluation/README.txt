Instructions:
	All code is called from testproject.py.  If all code files are contained in the same directory, a single call to the main function of testproject.py should generate all necessary reports and print all needed numerical statistics and metrics.

Submitted files:

indicators.py
	This file contains code to generate all of the indicators used previously in Project 6: Indicator Evaluation.  It contains functions that take in stock price data as a DataFrame and returns indicator values such as SMA, momentum, etc.  It is unmodified from that submission.
	
marketsimcode.py
	This file contains code that was orginally submitted as part of Project 5: Marketsim.  It contains functions that take in a DataFrame containing a series of stock trade orders indexed by date and computes and returns portfolio values for each date index.  It has been modified to include a new function that computes cumulative return, mean daily return, and standard deviation of daily return for use in the report for Project 8.

QLearner.py
	This file contains code for building, training, and running a general Q-learning model and was orginally submitted as part of Project 7: Q-Learning Robot.  It is unmodified from that submission.
	
ManualStrategy.py
	This file contains code for applying a rule-based stock trading strategy to a given stock price history.  It was written for this project and contains code to take in a series of stock price data and indicators implemented in indicators.py to develop and return a DataFrame of trades to make in that time period.  This file also contains the code that generates the figures illustrating Manual Strategy performance for in-sample and out-of-sample data.

StrategyLearner.py
	This file contains code for building, training, and running a Q-learning-based model tailored to make trading decisions based on the same set of indicators used in the Manual Strategy.  It calls functions in QLearner.py to develop the Q-learning model and computes stock position, return, and trades to pass to the Q-learning model and compile a list of trades to make on a series of stock price data.

experiment1.py
	This file contains code to run Experiment 1 and generate a figure for the report.  It tests both the Manual Strategy and Strategy Learner against the benchmark stock price and produces a figure illustrating their respective performance.

experiment2.py
	This file contains code to run Experiment 2 and generate a figure for the report.  It tests Strategy Learner using a series of varying values of impact to see its effect on the performance or behavior of Strategy Learner.  Its findings are used to generate a figure that illustrates the Strategy Learner's behavior.
	
testproject.py
	This file contains a code to produce all figures and numerical statistics included in the report.  It is intended to be used as a single endpoint to generate all required elements of the report in one function call.