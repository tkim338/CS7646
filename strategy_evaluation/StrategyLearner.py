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
        # self.num_bins = 3

        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission

        # self.learner = q.QLearner(alpha=0.5, gamma=0.5, rar=0.5, radr=0.99, num_states=5 ** 3, num_actions=3, dyna=0)
        # self.learner = q.QLearner(alpha=0.5, gamma=0.3, rar=0.8, radr=0.99, num_states=5 ** 3, num_actions=3)
        self.learner = q.QLearner(alpha=0.5, gamma=0.3, rar=0.8, radr=0.99, num_states=5 ** 3, num_actions=3)

        self.sym = None
        self.price_data = None
        self.sma20 = None
        self.sma50 = None
        self.bb_lower, self.bb_upper = None, None
        self.mm = None
        self.position = 1000

        self.states = None

    def setup(self, price_data):
        self.sym = price_data.columns[0]
        self.price_data = indicators.normalize(price_data)
        self.sma20 = indicators.sma(self.price_data, window_size=20)
        self.sma50 = indicators.sma(self.price_data, window_size=50)
        self.bb_lower, self.bb_upper = indicators.bollinger_bands(self.price_data)
        self.mm = indicators.momentum(self.price_data)

        sma = pd.cut(self.sma20['SMA'] - self.sma50['SMA'], 5, labels=False)

        bb_percent = (self.price_data[self.sym] - self.bb_lower['bb_lower']) / (self.bb_upper['bb_upper'] - self.bb_lower['bb_lower'])
        # bbp = pd.cut((self.price_data[self.sym] - self.bb_lower['bb_lower']) / (self.bb_upper['bb_upper'] - self.bb_lower['bb_lower']), self.num_bins, labels=False)
        # bbp = np.digitize((self.price_data[self.sym] - self.bb_lower['bb_lower']) / (self.bb_upper['bb_upper'] - self.bb_lower['bb_lower']), [-0.01, 1.01])
        bbp = pd.cut(bb_percent, 5, labels=False)

        # mm = pd.cut(self.mm['momentum'], self.num_bins, labels=False)
        # mm = np.digitize(self.mm['momentum'], [-2.5, 2.5])
        mm = pd.cut(self.mm['momentum'], 5, labels=False)

        self.states = sma*5**2 + bbp*5 + mm

    def update_position(self, action):
        # action: [0, 1, 2] = [hold, sell, buy]
        # position: [-1000, 1000] = [short, long]

        if action == 0: # no trade
            new_pos = self.position
        elif action == 1: # sell
            new_pos = -1000
        else: # buy
            new_pos = 1000
        trade = new_pos - self.position
        self.position = new_pos
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
        self.position = 1000

        states_df = pd.DataFrame(self.states.loc[self.states.first_valid_index():])
        states_df.columns = [0]
        p = price_data[self.sym][self.states.first_valid_index()]

        for i in range(0, 40):
            a = self.learner.querysetstate(int(states_df[0][0]))
            trade = self.update_position(a)

            for row in states_df.iterrows():
                date = row[0]
                p_prime = price_data[self.sym][date]
                delta = p_prime - p
                r = self.position * delta
                if trade != 0:  # trade made, pay fees
                    r -= self.commission
                    r -= abs(self.impact * p_prime)

                s = int(self.states[date])
                a = self.learner.query(s, r)
                trade = self.update_position(a)
                p = p_prime
  		  	   		     		  		  		    	 		 		   		 		  
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
        # output = {'Date': [sd, self.states.first_valid_index()], 'Trade': [0, 1000]}
        # self.position = 1000
        output = {'Date': [self.states.index[0]], 'Trade': [0]}
        self.position = 0

        price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=True)
        self.setup(pd.DataFrame(price_data[symbol]))

        # s = int(self.states[self.states.first_valid_index()])
        # a = self.learner.querysetstate(s)
        # self.update_position(a)


        counter = 51
        for td in price_data.iterrows():
            if counter > 0:
                counter -= 1
            else:
                date = td[0]
                s_prime = int(self.states[date])
                a = self.learner.querysetstate(s_prime)
                trade = self.update_position(a)

                if trade != 0:
                    output['Date'].append(date)
                    output['Trade'].append(trade)


        # cover final position
        output['Date'].append(self.states.index[-1])
        output['Trade'].append(-self.position)

        trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])

        if len(trades.values) == 0:
            date0 = self.price_data.index[0]
            val0 = 2000
            new_df = pd.DataFrame([val0], [date0], columns=[symbol])
            trades = trades.append(new_df)
        return trades  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		     		  		  		    	 		 		   		 		  
