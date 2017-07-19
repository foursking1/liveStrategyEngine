# -*- coding: utf-8 -*-
__author__ = 'foursking'
from exchange.subject import *
from exchange.Exchange import Exchange
from exchange.config import *
from trade.Account import Account
from trade.Ticker import Ticker
from trade.Depth import Depth
from trade.MarketOrder import MarketOrder
from trade.Order import *

class YunbiExchange(Exchange):

    subject = CNY_BTC
    platform = "huobi"
    label = "default"
    coinType = HUOBI_COIN_TYPE_BTC