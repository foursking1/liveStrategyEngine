# -*- coding: utf-8 -*-
__author__ = 'foursking'
from exchange.subject import *
from exchange.Exchange import Exchange
from trade.Account import Account
from trade.Ticker import Ticker
from trade.Depth import Depth
from trade.MarketOrder import MarketOrder
from trade.Order import *

import exchangeConnection.huobi.huobiService as HuobiService
import exchangeConnection.huobi.huobiServiceETH as HuobiServiceETH
from exchangeConnection.huobi.util import *
from exchangeConnection.huobi.utilETH import *
from utils.helper import *


class HuobiExchange():

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
            account.Balance = float(res['available_cny_display'])
            account.Stocks = float(res['available_btc_display'])
            account.FrozenBalance = float(res["frozen_cny_display"])
            account.FrozenStocks = float(res["frozen_btc_display"])
        if self.subject == CNY_LTC:
            res = HuobiService.getAccountInfo("cny", ACCOUNT_INFO)
            account.Balance = float(res['available_cny_display'])
            account.Stocks = float(res['available_ltc_display'])
            account.FrozenBalance = float(res["frozen_cny_display"])
            account.FrozenStocks = float(res["frozen_ltc_display"])
        if self.subject == CNY_ETH:
            res = HuobiServiceETH.get_balance()
            for item in res['data']['list']:
                if item['currency'] == 'cny' and item['type'] == 'trade':
                    account.Balance = float(item['balance'])
                elif item['currency'] == 'cny' and item['type'] == 'frozen':
                    account.FrozenBalance = float(item['balance'])
                elif item['currency'] == 'eth' and item['type'] == 'trade':
                    account.Stocks = float(item['balance'])
                elif item['currency'] == 'eth' and item['type'] == 'frozen':
                    account.FrozenStocks = float(item['balance'])

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

        if self.subject == CNY_ETH:
            pass
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

    def get_orders(self):
        orders = []
        ## todo: 只支持人民币市场
        if self.subject == CNY_BTC:
            res = HuobiService.getOrders(HUOBI_COIN_TYPE_BTC, CNY_MARKET, GET_ORDERS)
            for raw_orders in res:
                order = Order()
                order.Id = raw_orders['id']
                order.Amount = float(raw_orders['order_amount'])
                order.DealAmount = float(raw_orders['processed_amount'])
                order.Status = ORDER_STATE_PENDING
                order.Prices = float(raw_orders['order_price'])
                if raw_orders['type'] == 1:
                    order.Type = ORDER_TYPE_BUY
                elif raw_orders['type'] == 2:
                    order.Type = ORDER_TYPE_SELL
                orders.append(order)
        if self.subject == CNY_LTC:
            res = HuobiService.getOrders(HUOBI_COIN_TYPE_LTC, CNY_MARKET, GET_ORDERS)
            for raw_orders in res:
                order = Order()
                order.Id = raw_orders['id']
                order.Amount = float(raw_orders['order_amount'])
                order.DealAmount = float(raw_orders['processed_amount'])
                order.Status = ORDER_STATE_PENDING
                order.Prices = float(raw_orders['order_price'])
                if raw_orders['type'] == 1:
                    order.Type = ORDER_TYPE_BUY
                elif raw_orders['type'] == 2:
                    order.Type = ORDER_TYPE_SELL
                orders.append(order)
        return orders

    def get_order_info(self, id):
        order = Order()
        if self.subject == CNY_BTC:
            res = HuobiService.getOrderInfo(HUOBI_COIN_TYPE_BTC, id, CNY_MARKET, ORDER_INFO)
            order.Id = res['id']
            order.Amount = float(res['order_amount'])
            order.DealAmount = float(res['processed_amount'])
            order.Status = ORDER_STATE_PENDING
            order.Prices = float(res['order_price'])
            if res['type'] == 1:
                order.Type = ORDER_TYPE_BUY
            elif res['type'] == 2:
                order.Type = ORDER_TYPE_SELL

        if self.subject == CNY_LTC:
            res = HuobiService.getOrderInfo(HUOBI_COIN_TYPE_LTC, id, CNY_MARKET, ORDER_INFO)
            order.Id = res['id']
            order.Amount = float(res['order_amount'])
            order.DealAmount = float(res['processed_amount'])
            order.Status = ORDER_STATE_PENDING
            order.Prices = float(res['order_price'])
            if res['type'] == 1:
                order.Type = ORDER_TYPE_BUY
            elif res['type'] == 2:
                order.Type = ORDER_TYPE_SELL
        return order

    def sell(self, prices, amount, limit=True):
        if self.subject == CNY_BTC:
            if limit is True:
                res = HuobiService.sell(HUOBI_COIN_TYPE_BTC, prices, amount, None, None, CNY_MARKET, SELL)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1
            else:
                res = HuobiService.sellMarket(HUOBI_COIN_TYPE_BTC, amount, None, None, CNY_MARKET, SELL_MARKET)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1
        if self.subject == CNY_LTC:
            if limit is True:
                res = HuobiService.sell(HUOBI_COIN_TYPE_LTC, prices, amount, None, None, CNY_MARKET, SELL)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1
            else:
                res = HuobiService.sellMarket(HUOBI_COIN_TYPE_LTC, amount, None, None, CNY_MARKET, SELL_MARKET)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1

    def buy(self, prices, amount, limit=True):
        if self.subject == CNY_BTC:
            if limit is True:
                res = HuobiService.buy(HUOBI_COIN_TYPE_BTC, prices, amount, None, None, CNY_MARKET, BUY)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1
            elif limit is False:
                res = HuobiService.buyMarket(HUOBI_COIN_TYPE_BTC, amount, None, None, CNY_MARKET, BUY_MARKET)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1

        if self.subject == CNY_LTC:
            if limit is True:
                res = HuobiService.buy(HUOBI_COIN_TYPE_LTC, prices, amount, None, None, CNY_MARKET, BUY)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1
            elif limit is False:
                res = HuobiService.buyMarket(HUOBI_COIN_TYPE_LTC, amount, None, None, CNY_MARKET, BUY_MARKET)
                if res['result'] == "success":
                    return res['id']
                else:
                    return -1

    def cancel_order(self, id):
        if self.subject == CNY_BTC:
            res = HuobiService.cancelOrder(HUOBI_COIN_TYPE_BTC, id, CNY_MARKET, CANCEL_ORDER)
            if res['result'] == 'success':
                return True
            else:
                return False
        if self.subject == CNY_LTC:
            res = HuobiService.cancelOrder(HUOBI_COIN_TYPE_LTC, id, CNY_MARKET, CANCEL_ORDER)
            if res['result'] == 'success':
                return True
            else:
                return False

    def cancel_all(self):
        for order in self.get_orders():
            self.cancel_order(order.Id)







if __name__ == '__main__':
    exchange = HuobiExchange()
    exchange.switch_subject(CNY_ETH)
    account_info = exchange.get_account()
    ticker_info = exchange.get_ticker()
    depth_info = exchange.get_depth()
    orders = exchange.get_orders()
    print(account_info)
    print(ticker_info)
    print(depth_info)
    for order in orders:
        print(order)
        print(exchange.get_order_info(order.Id))

    id = exchange.buy(1, 0.01)
    print(exchange.get_order_info(id))
    exchange.cancel_all()
    orders = exchange.get_orders()
    for order in orders:
        print(order)
        print(exchange.get_order_info(order.Id))





