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
        # self.learner = q.QLearner(alpha=0.2, rar=0.9, radr=0.999, num_states=self.num_bins ** 4, num_actions=3, dyna=0)
        # self.learner = q.QLearner(alpha=0.2, gamma=0.5, rar=0.5, radr=0.99, num_states=self.num_bins ** 3, num_actions=3, dyna=0)

        # self.learner = q.QLearner(num_states=self.num_bins**2 * 3, num_actions=2, dyna=1000)
        self.learner = q.QLearner(alpha=0.5, gamma=0.5, rar=0.5, radr=0.99, num_states=self.num_bins ** 2 * 3 * 2, num_actions=3, dyna=1000)

        self.sym = None
        self.price_data = None
        self.sma20 = None
        self.sma50 = None
        self.bb_lower, self.bb_upper = None, None
        self.mm = None
        # self.vol = None
        self.position = 0

        self.states = None

    def setup(self, price_data):
        self.sym = price_data.columns[0]
        self.price_data = indicators.normalize(price_data)
        self.sma20 = indicators.sma(self.price_data, window_size=20)
        self.sma50 = indicators.sma(self.price_data, window_size=50)
        self.bb_lower, self.bb_upper = indicators.bollinger_bands(self.price_data)
        self.mm = indicators.momentum(self.price_data)
        # self.vol = indicators.volatility(self.price_data)

        # sma20_50 = pd.qcut(self.sma20['SMA'] - self.sma50['SMA'], self.num_bins, labels=False)
        # sma50_20 = pd.qcut(self.sma50['SMA'] - self.sma20['SMA'], self.num_bins, labels=False)

        sma20_val_prev = np.nan
        sma50_val_prev = np.nan
        sma = self.sma20
        for td in self.sma20.iterrows():
            date = td[0]
            sma20_val = self.sma20['SMA'][date]
            sma50_val = self.sma50['SMA'][date]
            # if date - dt.timedelta(days=1) in self.sma20['SMA']:
            #     sma20_val_prev = self.sma20['SMA'][date - dt.timedelta(days=1)]
            # else:
            #     sma20_val_prev = np.nan
            # if date - dt.timedelta(days=1) in self.sma50['SMA']:
            #     sma50_val_prev = self.sma50['SMA'][date - dt.timedelta(days=1)]
            # else:
            #     sma50_val_prev = np.nan

            if np.isnan(sma20_val) or np.isnan(sma50_val) or np.isnan(sma20_val_prev) or np.isnan(sma50_val_prev):
                sma['SMA'][date] = np.nan
            elif sma20_val > sma50_val and sma20_val_prev < sma50_val_prev:
                sma['SMA'][date] = 1
            elif sma20_val < sma50_val and sma20_val_prev > sma50_val_prev:
                sma['SMA'][date] = 2
            else:
                sma['SMA'][date] = 0

            sma20_val_prev = sma20_val
            sma50_val_prev = sma50_val

        # bbp = pd.qcut((self.price_data[self.sym] - self.bb_lower['bb_lower']) / (self.bb_upper['bb_upper'] - self.bb_lower['bb_lower']), self.num_bins, labels=False)
        bbp = pd.cut((self.price_data[self.sym] - self.bb_lower['bb_lower']) / (self.bb_upper['bb_upper'] - self.bb_lower['bb_lower']), self.num_bins, labels=False)

        # bb_upper = pd.qcut(self.price_data[self.sym] - self.bb_upper['bb_upper'], self.num_bins, labels=False)
        # bb_lower = pd.qcut(self.price_data[self.sym] - self.bb_lower['bb_lower'], self.num_bins, labels=False)

        # self.price_data = pd.qcut(self.price_data[self.sym], self.num_bins, labels=False)
        # self.sma20 = pd.qcut(self.sma20['SMA'], self.num_bins, labels=False)
        # self.sma50 = pd.qcut(self.sma50['SMA'], self.num_bins, labels=False)
        # self.bb_lower = pd.qcut(self.bb_lower['bb_lower'], self.num_bins, labels=False)
        # self.bb_upper = pd.qcut(self.bb_upper['bb_upper'], self.num_bins, labels=False)
        # mm = pd.qcut(self.mm['momentum'], self.num_bins, labels=False)
        mm = pd.cut(self.mm['momentum'], self.num_bins, labels=False)

        # self.states = sma20_50*3**4 + sma50_20*3**3 + bb_lower*3**2 + bb_upper*3 + self.mm
        # self.states = sma['SMA']*3**3 + bb_upper*3**2 + bb_lower*3**1 + self.mm
        self.states = sma['SMA']*3*self.num_bins + bbp*self.num_bins + mm

    def update_position(self, action):
        if action == 0:
            trade = -1000 - 1000 * self.position
            self.position = 0
        elif action == 1:
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

        states_df = pd.DataFrame(self.states.loc[self.states.first_valid_index():])
        p = price_data[self.sym][self.states.first_valid_index()]
        a = 2
        for row in states_df.iterrows():
            date = row[0]
            p_prime = price_data[self.sym][date]
            delta = p_prime - p
            r = (self.position*2-1) * delta
            if a != 2:  # trade made, pay fees
                r -= self.commission
                r -= abs(self.impact * p_prime)

            s = int(self.states[date]) + (self.position * self.num_bins ** 2 * 3)
            a = self.learner.query(s, r)
            self.update_position(a)
            p = p_prime

        # for i in range(0, 1):
        #     date = self.states.first_valid_index()
        #     s0 = int(self.states[date])
        #     a = self.learner.querysetstate(s0)
        #     self.update_position(a)
        #     p = price_data[self.sym][date]
        #     date += dt.timedelta(days=1)
        #
        #     date_final = self.states.last_valid_index()
        #     while date <= date_final:
        #         if date in price_data[self.sym]:
        #             p_prime = price_data[self.sym][date]
        #             delta = p_prime - p
        #             r = self.position * delta
        #             if a != 2: # trade made
        #                 r -= self.commission
        #                 r -= abs(self.impact * p_prime)
        #
        #             s = int(self.states[date])
        #             a = self.learner.query(s, r)
        #             self.update_position(a)
        #             p = p_prime
        #         date += dt.timedelta(days=1)
  		  	   		     		  		  		    	 		 		   		 		  
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
                trade = 1 * self.update_position(a)

                if trade != 0:
                    output['Date'].append(date - dt.timedelta(days=1))
                    output['Trade'].append(trade)


        # output['Trade'] = []
        # output['Date'] = []

        trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])

        if len(trades.values) == 0:
            date0 = self.price_data.index[0]
            val0 = 2000
            new_df = pd.DataFrame([val0], [date0], columns=[symbol])
            trades = trades.append(new_df)
        return trades  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		     		  		  		    	 		 		   		 		  
