#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'foursking'

class MarketOrder(object):
    Price = 0.0
    Amount = 0.0

    def __init__(self, price, amount):
        self.Price = float(price)
        self.Amount = float(amount)

    def __str__(self):
        return "价格 %f, 数量 %f" % (self.Price, self.Amount)
