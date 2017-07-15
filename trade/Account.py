#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'foursking'

class Account(object):

    Balance = 0.0
    Stocks = 0.0

    FrozenBalance = 0.0
    FrozenStocks = 0.0

    def __init__(self, Balance, Stocks, FrozenBalance, FrozenStocks):
        self.Balance = float(Balance)
        self.Stocks = float(Stocks)
        self.FrozenBalance = float(FrozenBalance)
        self.FrozenStocks = float(FrozenStocks)

    def __str__(self):
        return("法币%f,  股票 %f， 冻结的法币%f,  冻结的股票%f" %
               (self.Balance, self.Stocks, self.FrozenBalance, self.FrozenStocks))



if __name__ == '__main__':
    account = Account()
    pass




