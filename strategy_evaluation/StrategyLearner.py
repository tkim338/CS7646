""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
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
import random  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
import util as ut
import QLearner as q
import indicators
import numpy as np





class StrategyLearner(object):
    """  		  	   		     		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		     		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		     		  		  		    	 		 		   		 		  
    """
    def author(self):
        return 'tkim338'

    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """
        self.num_bins = 3

        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission
        self.learner = q.QLearner(alpha=0.8, rar=0.99, radr=0.999, num_states=self.num_bins**6 * 3, num_actions=3, dyna=1000)

        self.sym = None
        self.price_data = None
        self.sma20 = None
        self.sma50 = None
        self.bb_lower, self.bb_upper = None, None
        self.mm = None
        # self.vol = None
        self.position = 0

    def setup(self, price_data):
        self.sym = price_data.columns[0]
        self.price_data = indicators.normalize(price_data)
        self.sma20 = indicators.sma(self.price_data, window_size=20)
        self.sma50 = indicators.sma(self.price_data, window_size=50)
        self.bb_lower, self.bb_upper = indicators.bollinger_bands(self.price_data)
        self.mm = indicators.momentum(self.price_data)
        # self.vol = indicators.volatility(self.price_data)

    def bin(self, data):
        div = 2 / self.num_bins # (-1, 1) input
        if np.isnan(data):
            return None

        bins = np.arange(-div, 1.1, div)
        return np.min([np.sum(bins < data) - 1, self.num_bins - 1])

        # if data < -div:
        #     return 0
        # if data < 0:
        #     return 1
        # if data < 0.5:
        #     return 2
        # return 3

    def get_state(self, date):
        s = []
        s.append(self.bin(self.price_data[self.sym][date]))
        # s.append(self.bin(self.sma20['SMA'][date]))
        # s.append(self.bin(self.sma50['SMA'][date]))
        s.append(self.bin(self.sma20['SMA'][date] - self.sma50['SMA'][date]))
        s.append(self.bin(self.sma50['SMA'][date] - self.sma20['SMA'][date]))

        # s.append(self.bin(self.bb_lower['bb_lower'][date]))
        # s.append(self.bin(self.bb_upper['bb_upper'][date]))
        s.append(self.bin(self.price_data[self.sym][date] - self.bb_upper['bb_upper'][date]))
        s.append(self.bin(self.price_data[self.sym][date] - self.bb_lower['bb_lower'][date]))

        s.append(self.bin(self.mm['momentum'][date]))
        s.append(self.position + 1)
        if any(si is None for si in s):
            return 0
        state = 0
        for i in range(len(s)):
            state += s[i] * self.num_bins**i
        return state

    def update_position(self, action):
        if action == 0:
            trade = -1000 - 1000 * self.position
            self.position = -1
        elif action == 2:
            trade = 1000 - 1000 * self.position
            self.position = 1
        else:
            trade = 0
        return trade

    # this method should create a QLearner, and train it for trading  		  	   		     		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		     		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		     		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		     		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		     		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		     		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        # add your code to do learning here
        price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=True)
        self.setup(pd.DataFrame(price_data[symbol]))

        s = self.get_state(price_data.first_valid_index())
        a = self.learner.querysetstate(s)
        self.update_position(a)
        p = price_data[symbol][0]

        counter = 51
        for td in price_data.iterrows():
            if counter > 0:
                counter -= 1
            else:
                date = td[0]
                p_prime = td[1][symbol]
                delta = p_prime - p
                r = self.position * delta
                s_prime = self.get_state(date)
                a = self.learner.query(s_prime, r)
                self.update_position(a)
  		  	   		     		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		     		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		     		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		     		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		     		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		     		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		     		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		     		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		     		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		     		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		     		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		     		  		  		    	 		 		   		 		  
        """
        output = {'Date': [], 'Trade': []}

        price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=True)
        self.setup(pd.DataFrame(price_data[symbol]))

        s = self.get_state(price_data.first_valid_index())
        a = self.learner.querysetstate(s)
        self.update_position(a)

        counter = 51
        for td in price_data.iterrows():
            if counter > 0:
                counter -= 1
            else:
                date = td[0]
                s_prime = self.get_state(date)
                a = self.learner.querysetstate(s_prime)
                trade = self.update_position(a)

                if trade != 0:
                    output['Date'].append(date)
                    output['Trade'].append(trade)
        trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])
        return trades  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		     		  		  		    	 		 		   		 		  
