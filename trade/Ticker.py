#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'foursking'

class Ticker(object):

    Sell = 0.0
    Volume = 0.0
    Buy = 0.0
    Last = 0.0
    High = 0.0
    Low = 0.0
    Open = 0.0

    def __init__(self, buy, sell, high, low, volume, open, last ):
        self.Sell = float(sell)
        self.Volume = float(volume)
        self.Buy = float(buy)
        self.Open = float(open)
        self.Last = float(last)
        self.High = float(high)
        self.Low = float(low)

    def __str__(self):
        return("开盘价 %f， 收盘价 %f， 买一价 %f， 卖一价 %f， 最高价 %f， 最低价 %f， 成交量 %f" % (
            self.Open, self.Last, self.Buy, self.Sell, self.High, self.Low, self.Volume
        ))

