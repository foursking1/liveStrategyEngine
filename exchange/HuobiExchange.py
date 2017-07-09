__author__ = 'foursking'
from exchange.subject import *
from trade.Account import Account
from trade.Ticker import Ticker
from trade.Depth import Depth
from trade.MarketOrder import MarketOrder

import exchangeConnection.huobi.huobiService as HuobiService
from exchangeConnection.huobi.util import *
from utils.helper import *

class HuobiExchange:

    subject = CNY_BTC
    platform = "huobi"
    label = "default"

    def set_label(self, label):
        self.label = label

    def switch_subject(self, subject):
        self.subject = subject

    def get_currency(self):
        return self.subject

    def get_label(self):
        return self.label

    def get_name(self):
        return "平台是 %s, 标的是 %s" % (self.platform, self.subject)

    def get_account(self):
        account = Account()
        if self.subject == CNY_BTC:
            res = HuobiService.getAccountInfo("cny", ACCOUNT_INFO)
            account.Balance = res['available_cny_display']
            account.Stocks = res['available_btc_display']
            account.FrozenBalance = res["frozen_cny_display"]
            account.FrozenStocks = res["frozen_btc_display"]
        if self.subject == CNY_LTC:
            res = HuobiService.getAccountInfo("cny", ACCOUNT_INFO)
            account.Balance = res['available_cny_display']
            account.Stocks = res['available_ltc_display']
            account.FrozenBalance = res["frozen_cny_display"]
            account.FrozenStocks = res["frozen_ltc_display"]
        return account

    def get_ticker(self):
        ticker = Ticker()
        if self.subject == CNY_BTC:
            res = HuobiService.getTicker(HUOBI_COIN_TYPE_BTC, "cny")
            ticker.Buy = res['ticker']['buy']
            ticker.Sell = res['ticker']['sell']
            ticker.High = res['ticker']['high']
            ticker.Low = res['ticker']['low']
            ticker.Volume = res['ticker']['vol']
            ticker.open = res['ticker']['open']
            ticker.Last = res['ticker']['last']
            assert res['ticker']['symbol'] == 'btccny'

        if self.subject == CNY_LTC:
            res = HuobiService.getTicker(HUOBI_COIN_TYPE_LTC, "cny")
            ticker.Buy = res['ticker']['buy']
            ticker.Sell = res['ticker']['sell']
            ticker.High = res['ticker']['high']
            ticker.Low = res['ticker']['low']
            ticker.Volume = res['ticker']['vol']
            ticker.open = res['ticker']['open']
            ticker.Last = res['ticker']['last']
            assert res['ticker']['symbol'] == "ltccny"

        return ticker

    def get_depth(self, depth_size=5):
        depth = Depth()
        if self.subject == CNY_BTC:
            res = HuobiService.getDepth(HUOBI_COIN_TYPE_BTC, "cny", depth_size)
            for bids in res['bids']:
                market_order = MarketOrder()
                market_order.Price = bids[0]
                market_order.Amount = bids[1]
                depth.Bids.append(market_order)
            for asks in res['asks']:
                market_order = MarketOrder()
                market_order.Price = asks[0]
                market_order.Amount = asks[1]
                depth.Asks.append(market_order)

        if self.subject == CNY_LTC:
            res = HuobiService.getDepth(HUOBI_COIN_TYPE_LTC, "cny", depth_size)
            for bids in res['bids']:
                market_order = MarketOrder()
                market_order.Price = bids[0]
                market_order.Amount = bids[1]
                depth.Bids.append(market_order)
            for asks in res['asks']:
                market_order = MarketOrder()
                market_order.Price = asks[0]
                market_order.Amount = asks[1]
                depth.Asks.append(market_order)
        return depth

    def get_trades(self):
        pass

if __name__ == '__main__':
    exchange = HuobiExchange()
    account_info = exchange.get_account()
    ticker_info = exchange.get_ticker()
    depth_info = exchange.get_depth()
    print(account_info)
    print(ticker_info)
    print(depth_info)




