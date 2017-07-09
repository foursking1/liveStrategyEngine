#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'foursking'

class Account(object):

    Balance = 0.0
    Stocks = 0.0

    FrozenBalance = 0.0
    FrozenStocks = 0.0

    def __str__(self):
        return("法币%s,  股票 %s， 冻结的法币%s,  冻结的股票%s" %
               (self.Balance, self.Stocks, self.FrozenBalance, self.FrozenStocks))



if __name__ == '__main__':
    account = Account()
    pass




