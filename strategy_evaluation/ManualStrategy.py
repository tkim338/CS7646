import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import indicators
import csv
import marketsimcode as msc
import matplotlib.pyplot as plt

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

    # def date_list(self, sd, ed):
    #     all_dates = []
    #     day_increment = dt.timedelta(days=1)
    #     date_i = sd
    #     while date_i <= ed:
    #         all_dates.append(date_i)
    #         date_i += day_increment
    #     return all_dates

    def setup(self, price_data):
        self.sym = price_data.columns[0]
        self.price_data = indicators.normalize(price_data)
        self.sma20 = indicators.sma(self.price_data, window_size=20)
        self.sma50 = indicators.sma(self.price_data, window_size=50)
        self.bb_lower, self.bb_upper = indicators.bollinger_bands(self.price_data)
        self.mm = indicators.momentum(self.price_data)
        # self.vol = indicators.volatility(self.price_data)

    def get_signal(self, date, prev_date):
        signal = []
        # check SMA
        if prev_date and prev_date in self.sma20['SMA'] and prev_date in self.sma50['SMA']:
            if self.sma20['SMA'][prev_date] < self.sma50['SMA'][prev_date] and self.sma20['SMA'][date] > self.sma50['SMA'][date]:
                signal.append(1)
            if self.sma20['SMA'][prev_date] > self.sma50['SMA'][prev_date] and self.sma20['SMA'][date] < self.sma50['SMA'][date]:
                signal.append(-1)

        # check Bollinger Band
        bbp = (self.price_data[self.sym][date] - self.bb_lower['bb_lower'][date]) / (self.bb_upper['bb_upper'][date] - self.bb_lower['bb_lower'][date])
        if bbp < -0.01:
            signal.append(1)
        elif bbp > 1.01:
            signal.append(-1)

        # check momentum
        if self.mm['momentum'][date] > 2.5:
            signal.append(1)
        if self.mm['momentum'][date] < -2.5:
            signal.append(-1)

        if signal:
            if np.sum(signal) > 0:
                return 1
            elif np.sum(signal) < 0:
                return -1
        return 0

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        # stock_data = get_data([symbol], all_dates, addSPY=False)
        stock_data = get_data([symbol], pd.date_range(sd, ed), addSPY=True)
        current_position = 0
        output = {'Date': [], 'Trade': []}
        self.setup(pd.DataFrame(stock_data[symbol]))

        # for date in all_dates:
        prev_date = None
        for row in self.price_data.iterrows():
            date = row[0]
            price = stock_data[symbol][date]

            if not np.isnan(price) and not np.isnan(stock_data['SPY'][date]):
                signal = self.get_signal(date, prev_date)

                if signal == 1:
                    trade = 1000 - current_position
                    current_position = 1000
                elif signal == -1:
                    trade = -1000 - current_position
                    current_position = -1000
                else:
                    # trade = -current_position
                    # current_position = 0
                    trade = 0

                if trade != 0:
                    output['Date'].append(date)
                    output['Trade'].append(trade)
            prev_date = date

        # cover final position
        # output['Date'].append(all_dates[-1])
        # output['Trade'].append(-current_position)
        # current_position = 0

        df_trades = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[symbol])

        return df_trades

    def benchmark(self, benchmark_symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        stock_data = get_data([benchmark_symbol], pd.date_range(sd, ed), addSPY=False)

        buy_date = stock_data[benchmark_symbol].first_valid_index()
        sell_date = stock_data[benchmark_symbol].last_valid_index()

        output = {'Date': [], 'Trade': []}
        output['Date'] = [buy_date, sell_date]
        output['Trade'] = [1000, -1000]

        df_benchmark = pd.DataFrame(data=output['Trade'], index=output['Date'], columns=[benchmark_symbol])

        return df_benchmark

    def sample_test(self, sym, start_date, end_date, filename):
        trades_man = self.testPolicy(symbol=sym, sd=start_date, ed=end_date)
        vals_man = msc.compute_portvals(trades_man, start_val=100000, commission=9.95, impact=0.005)
        vals_man = vals_man / vals_man[0][0]
        vals_man.columns = ['manual strategy']

        trades_bm = self.benchmark(sym, start_date, end_date)
        vals_bm = msc.compute_portvals(trades_bm, start_val=100000, commission=9.95, impact=0.005)
        vals_bm = vals_bm / vals_bm[0][0]
        vals_bm.columns = ['benchmark']

        output = pd.DataFrame([vals_bm['benchmark'], vals_man['manual strategy']]).transpose()
        output = output.fillna(method='ffill')
        output = output.fillna(method='bfill')
        output_plot = output.plot(color=['g', 'r'], figsize=(15,8))
        output_plot.set_xlabel('Date')
        output_plot.set_ylabel('Normalized Value')
        output_plot.grid(b=True, which='both', axis='both')

        y_min = output_plot.dataLim.min[1]
        y_max = output_plot.dataLim.max[1]
        for index, data in trades_man.iterrows():
            if data[sym] > 0:
                output_plot.plot([index, index], [y_min, y_max], 'b', linewidth=1)
            else:
                output_plot.plot([index, index], [y_min, y_max], 'k', linewidth=1)

        plt.savefig(filename)
        return vals_man['manual strategy'] / vals_bm['benchmark']

    def in_sample_test(self):
        sym = 'JPM'
        start_date = dt.datetime(2008, 1, 1)
        end_date = dt.datetime(2009, 12, 31)
        filename = 'in-sample-test.png'
        df = self.sample_test(sym, start_date, end_date, filename)
        df = df.fillna(method='bfill')
        df = df.fillna(method='ffill')
        return df

    def out_sample_test(self):
        sym = 'JPM'
        start_date = dt.datetime(2010, 1, 1)
        end_date = dt.datetime(2011, 12, 31)
        filename = 'out-sample-test.png'
        df = self.sample_test(sym, start_date, end_date, filename)
        df = df.fillna(method='bfill')
        df = df.fillna(method='ffill')
        return df