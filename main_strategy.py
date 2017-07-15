# !/usr/bin/env python
# -*- coding: utf-8 -*-


import userStrategy.Compare as Compare
from liveStrategyEngine.BaseMultipleStartegyEngine import BaseMultiLiveStrategyEngine
from exchange.HuobiExchange import HuobiExchange
from utils.helper import *


if __name__ == "__main__":

    exchanges = [HuobiExchange]
    strat = BaseMultiLiveStrategyEngine(Compare, exchanges, 1, datetime.datetime.now(), 0.1, 30,
                                        dailyExitTime="23:30:00")
    start_strat(strat)
