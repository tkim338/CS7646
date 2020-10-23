import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import indicators
import csv

class ManualStrategy:

    def author(self):
        return 'tkim338'

    def __init__(self):
        self.sym = None
        self.price_data = None
        self.sma20 = None
        self.sma50 = None
        self.bb_lower, self.bb_upper = None, None
        self.mm = None
        self.vol = None

    def date_list(self, sd, ed):
        all_dates = []
        day_increment = dt.timedelta(days=1)
        date_i = sd
        while date_i <= ed:
            all_dates.append(date_i)
            date_i += day_increment
        return all_dates

    def setup(self, price_data):
        self.sym = price_data.columns[0]
        self.price_data = indicators.normalize(price_data)
        self.sma20 = indicators.sma(self.price_data, window_size=20)
        self.sma50 = indicators.sma(self.price_data, window_size=50)
        self.bb_lower, self.bb_upper = indicators.bollinger_bands(self.price_data)
        self.mm = indicators.momentum(self.price_data)
        self.vol = indicators.volatility(self.price_data)

    def get_signal(self, date):
        signal = []
        # check SMA
        prev_date = date - dt.timedelta(days=1)
        if prev_date in self.sma20['SMA'] and prev_date in self.sma50['SMA']:
            if self.sma20['SMA'][prev_date] < self.sma50['SMA'][prev_date] and self.sma20['SMA'][date] > self.sma50['SMA'][date]:
                signal.append(1)
            if self.sma20['SMA'][prev_date] > self.sma50['SMA'][prev_date] and self.sma20['SMA'][date] < self.sma50['SMA'][date]:
                signal.append(-1)

        # check Bollinger Band
        if self.price_data[self.sym][date] < self.bb_lower['bb_lower'][date]:
            signal.append(1)
        if self.price_data[self.sym][date] > self.bb_upper['bb_upper'][date]:
            signal.append(-1)

        # check momentum
        if self.mm['momentum'][date] > 0:
            signal.append(-1)
        if self.mm['momentum'][date] < 0:
            signal.append(1)

        if signal:
            if np.sum(signal) > 0:
                return 1
            elif np.sum(signal) < 0:
                return -1
        return 0

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        all_dates = self.date_list(sd, ed)
        # stock_data = get_data([symbol], all_dates, addSPY=False)
        stock_data = get_data([symbol], pd.date_range(sd, ed), addSPY=True)
        current_position = 0
        output = {'Date': [], 'Trade': []}
        self.setup(pd.DataFrame(stock_data[symbol]))

        # for date in all_dates:
        for row in self.price_data.iterrows():
            date = row[0]
            price = stock_data[symbol][date]

            if not np.isnan(price) and not np.isnan(stock_data['SPY'][date]):
                signal = self.get_signal(date)

                if signal == 1:
                    trade = 1000 - current_position
                    current_position = 1000
                elif signal == -1:
                    trade = -1000 - current_position
                    current_position = -1000
                else:
                    trade = -current_position
                    current_position = 0

                if trade != 0:
                    output['Date'].append(date)
                    output['Trade'].append(trade)

        # cover final position
        # output['Date'].append(all_dates[-1])
        # output['Trade'].append(-current_position)
        # current_position = 0

        df_trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])

        return df_trades