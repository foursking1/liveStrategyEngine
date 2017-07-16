#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'foursking'

TRADE_TYPE_BUY = 1
TRADE_TYPE_SELL = 2
TRADE_TYPE_UNDEFINED = 3

class Trade(object):

    Time = 0
    Price = 0
    Amount = 0
    TradeType = 0

    def __init__(self, time, price, amount, trade_type):
        self.Time = time
        self.Price = float(price)
        self.Amount = float(amount)
        self.TradeType = int(trade_type)

    def __str__(self):

        if self.TradeType == TRADE_TYPE_BUY:
            trade_type = "买"
        elif self.TradeType == TRADE_TYPE_SELL:
            trade_type = "卖"
        else:
            trade_type = "未知"

        return("时间戳 %s， 成交价 %f， 成交量 %f， 交易类型 %s" % (
            self.Time, self.Price, self.Amount, trade_type))