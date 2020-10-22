from agent.TradingAgent import TradingAgent
import pandas as pd
import numpy as np
import os
from contributed_traders.util import get_file

import csv

class tkim338_monkey(TradingAgent):

    def __init__(self, id, name, type, symbol, starting_cash,
                 min_size, max_size, wake_up_freq='60s',
                 log_orders=False, random_state=None):

        super().__init__(id, name, type, starting_cash=starting_cash, log_orders=log_orders, random_state=random_state)
        self.symbol = symbol
        self.min_size = min_size  # Minimum order size
        self.max_size = max_size  # Maximum order size
        # self.size = self.random_state.randint(self.min_size, self.max_size)
        self.size = max_size
        self.wake_up_freq = wake_up_freq
        self.log_orders = log_orders
        self.state = "AWAITING_WAKEUP"

        # Bollinger Bands
        self.window_size = {'small': 20, 'large': 50}
        # self.history = {'ask': {'small': [], 'large': []}, 'bid': {'small': [], 'large': []}}
        self.history = {'small': [], 'large': []}
        self.prev_sma = {'small': 0, 'large': 0}

        self.debug = {'shares': [], 'price': [], 'time': [], 'price_history': []}

    def kernelStarting(self, startTime):
        super().kernelStarting(startTime)
        # Read in the configuration through util
        with open(get_file('tkim338_monkey/monkey.cfg'), 'r') as f:
            self.window1, self.window2 = [int(w) for w in f.readline().split()]
        #print(f"{self.window1} {self.window2}")

    def wakeup(self, currentTime):
        """ Agent wakeup is determined by self.wake_up_freq """
        can_trade = super().wakeup(currentTime)
        if not can_trade: return
        self.getCurrentSpread(self.symbol)
        self.state = 'AWAITING_SPREAD'

    def dump_shares(self):
        # get rid of any outstanding shares we have
        if self.symbol in self.holdings and len(self.orders) == 0:
            order_size = self.holdings[self.symbol]
            bid, _, ask, _ = self.getKnownBidAsk(self.symbol)
            if bid:
                self.placeLimitOrder(self.symbol, quantity=order_size, is_buy_order=False, limit_price=0)

                self.debug['shares'].append(-1 * order_size)
                self.debug['price'].append(bid)
                self.debug['time'].append('end')

    def receiveMessage(self, currentTime, msg):
        super().receiveMessage(currentTime, msg)
        if self.state == 'AWAITING_SPREAD' and msg.body['msg'] == 'QUERY_SPREAD':
            dt = (self.mkt_close - currentTime) / np.timedelta64(1, 'm')
            if dt < 5:
                self.dump_shares()
            else:
                bid, bid_vol, ask, ask_vol = self.getKnownBidAsk(self.symbol)
                if bid and ask:
                    self.debug['price_history'].append(np.mean([bid, ask]))

                    sma = {'small': 0, 'large': 0}
                    bb = {'small': (), 'large': ()}

                    for size in ['small', 'large']:
                        self.history[size].append(np.mean([ask, bid]))

                        if len(self.history[size]) > self.window_size[size]:
                            self.history[size].pop(0)

                        # compute SMA
                        sma[size] = np.mean(self.history[size])

                        # compute Bollinger Band
                        bb[size] = (sma[size] - 2 * np.std(self.history[size]), sma[size] + 2 * np.std(self.history[size]))

                    if len(self.history['large']) >= self.window_size['large']:
                        signal = [0, 0, 0]
                        # check SMA
                        # if self.prev_sma['small'] < self.prev_sma['large'] and sma['small'] > sma['large']:
                        #     signal[0] = 1
                        # if self.prev_sma['small'] > self.prev_sma['large'] and sma['small'] < sma['large']:
                        #     signal[0] = -1
                        # self.prev_sma['small'] = sma['small']
                        # self.prev_sma['large'] = sma['large']

                        # check Bollinger Band
                        if ask < bb['small'][0] and bid < bb['small'][0]:
                            signal[1] = 1
                        if ask > bb['small'][1] and bid > bb['small'][1]:
                            signal[1] = -1

                        # check momentum
                        # if mm['ask']['large'] > 0 and mm['bid']['large'] > 0:
                        #     signal[2] = 1
                        # if mm['ask']['large'] < 0 and mm['bid']['large'] < 0:
                        #     signal[2] = -1

                        for i in range(10):
                            if signal[1] == 1:
                                self.placeLimitOrder(self.symbol, quantity=self.size, is_buy_order=True, limit_price=ask)
                                self.debug['shares'].append(self.size)
                                self.debug['price'].append(ask)
                                self.debug['time'].append(currentTime)
                            if signal[1] == -1:
                                self.placeLimitOrder(self.symbol, quantity=self.size, is_buy_order=False, limit_price=bid)
                                self.debug['shares'].append(-1 * self.size)
                                self.debug['price'].append(bid)
                                self.debug['time'].append(currentTime)

            self.setWakeup(currentTime + self.getWakeFrequency())
            self.state = 'AWAITING_WAKEUP'

    def getWakeFrequency(self):
        return pd.Timedelta(self.wake_up_freq)

    def author(self):
        return 'tkim338'