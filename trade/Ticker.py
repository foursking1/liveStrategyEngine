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

    def __str__(self):
        return("开盘价 %s， 收盘价 %s， 买一价 %s， 卖一价 %s， 最高价 %s， 最低价 %s， 成交量 %s" % (
            self.Open, self.Last, self.Buy, self.Sell, self.High, self.Low, self.Volume
        ))

