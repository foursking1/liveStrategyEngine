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
from exchange.config import *


class HuobiExchange(Exchange):

    subject = CNY_BTC
    platform = "huobi"
    label = "default"
    coinType = HUOBI_COIN_TYPE_BTC

    def set_label(self, label):
        self.label = label

    def switch_subject(self, subject):
        if subject == CNY_BTC:
            self.coinType = HUOBI_COIN_TYPE_BTC
        elif subject == CNY_LTC:
            self.coinType = HUOBI_COIN_TYPE_LTC
        elif subject == CNY_ETH:
            self.coinType = HUOBI_COIN_TYPE_ETH
        elif subject == CNY_ETC:
            self.coinType = HUOBI_COIN_TYPE_ETC
        else:
            raise NotImplementedError
        self.subject = subject

    def get_currency(self):
        return self.subject

    def get_label(self):
        return self.label

    def get_name(self):
        return "平台是 %s, 标的是 %s" % (self.platform, self.subject)

    def get_account(self):
        try:
            balance, frozenBalance, stocks, frozenStocks = 0, 0, 0, 0
            if self.subject == CNY_BTC:
                res = HuobiService.getAccountInfo("cny", ACCOUNT_INFO)
                balance = float(res['available_cny_display'])
                stocks = float(res['available_btc_display'])
                frozenBalance = float(res["frozen_cny_display"])
                frozenStocks = float(res["frozen_btc_display"])

            if self.subject == CNY_LTC:
                res = HuobiService.getAccountInfo("cny", ACCOUNT_INFO)
                balance = float(res['available_cny_display'])
                stocks = float(res['available_ltc_display'])
                frozenBalance = float(res["frozen_cny_display"])
                frozenStocks = float(res["frozen_ltc_display"])

            if self.subject == CNY_ETH:
                res = HuobiServiceETH.get_balance()
                for item in res['data']['list']:
                    if item['currency'] == 'cny' and item['type'] == 'trade':
                        balance = float(item['balance'])
                    elif item['currency'] == 'cny' and item['type'] == 'frozen':
                        frozenBalance = float(item['balance'])
                    elif item['currency'] == 'eth' and item['type'] == 'trade':
                        stocks = float(item['balance'])
                    elif item['currency'] == 'eth' and item['type'] == 'frozen':
                        frozenStocks = float(item['balance'])

            if self.subject == CNY_ETC:
                res = HuobiServiceETH.get_balance()
                for item in res['data']['list']:
                    if item['currency'] == 'cny' and item['type'] == 'trade':
                        balance = float(item['balance'])
                    elif item['currency'] == 'cny' and item['type'] == 'frozen':
                        frozenBalance = float(item['balance'])
                    elif item['currency'] == 'etc' and item['type'] == 'trade':
                        stocks = float(item['balance'])
                    elif item['currency'] == 'etc' and item['type'] == 'frozen':
                        frozenStocks = float(item['balance'])

            account = Account(balance, stocks, frozenBalance, frozenStocks)
            return account
        except:
            return None

    def get_ticker(self):
        try:
            buy, sell, high, low, volume, open, last = 0, 0, 0, 0, 0, 0, 0
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                res = HuobiService.getTicker(self.coinType, "cny")
                buy = res['ticker']['buy']
                sell = res['ticker']['sell']
                high = res['ticker']['high']
                low = res['ticker']['low']
                volume = res['ticker']['vol']
                open = res['ticker']['open']
                last = res['ticker']['last']

            elif self.subject == CNY_ETH or self.subject == CNY_ETC:
                res  = HuobiServiceETH.get_ticker(self.coinType)
                buy = res['tick']['bid'][0]
                sell = res['tick']['ask'][0]
                high = res['tick']['high']
                low = res['tick']['low']
                volume = res['tick']['vol']
                open = res['tick']['open']
                last = res['tick']['close']

            ticker = Ticker(buy, sell, high, low, volume, open, last)
            return ticker
        except:
            return None

    def get_depth(self, depth_size=5):
        try:
            bids = []
            asks = []
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                res = HuobiService.getDepth(self.coinType, "cny", depth_size)
                for bids in res['bids']:
                    price, amount = float(bids[0]), float(bids[1])
                    market_order = MarketOrder(price, amount)
                    bids.append(market_order)
                for asks in res['asks']:
                    price, amount = float(asks[0]), float(asks[1])
                    market_order = MarketOrder(price, amount)
                    asks.append(market_order)

            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                res = HuobiServiceETH.get_depth(self.coinType, 'step0')
                for bids in res['tick']['bids']:
                    price, amount = float(bids[0]), float(bids[1])
                    market_order = MarketOrder(price, amount)
                    bids.append(market_order)
                for asks in res['tick']['asks']:
                    price, amount = float(asks[0]), float(asks[1])
                    market_order = MarketOrder(price, amount)
                    asks.append(market_order)

            depth = Depth(bids, asks)
            return depth
        except:
            return None

    # 获取所有交易历史
    def get_trades(self):
        pass

    def get_orders(self):
        try:
            orders = []
            id, amount, deal_amount, status, prices, type = 0, 0, 0, 0, 0, 0
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                res = HuobiService.getOrders(self.coinType, CNY_MARKET, GET_ORDERS)
                for raw_orders in res:
                    id = raw_orders['id']
                    amount = float(raw_orders['order_amount'])
                    deal_amount = float(raw_orders['processed_amount'])
                    status = ORDER_STATE_PENDING
                    prices = float(raw_orders['order_price'])
                    if raw_orders['type'] == 1:
                        type = ORDER_TYPE_BUY
                    elif raw_orders['type'] == 2:
                        type = ORDER_TYPE_SELL
                    order = Order(id, amount, prices, deal_amount, status, type)
                    orders.append(order)
            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                res = HuobiServiceETH.orders_list(self.coinType, 'submitted')
                for raw_orders in res['data']:
                    id = raw_orders['id']
                    amount = raw_orders['amount']
                    deal_amount = raw_orders['field-amount']
                    state = raw_orders['state']
                    if state is 'submitted' or state is 'partial-filled':
                        status = ORDER_STATE_PENDING
                    elif state is 'canceled':
                        status = ORDER_STATE_CANCELED
                    elif state is 'filled':
                        status = ORDER_STATE_CLOSED
                    if raw_orders['type'] is "buy-market" or raw_orders['type'] is "buy-limit":
                        type = ORDER_TYPE_BUY
                    elif raw_orders['type'] is "sell-market" or raw_orders['type'] is "sell-limit":
                        type = ORDER_TYPE_SELL
                    order = Order(id, amount, prices, deal_amount, status, type)
                    orders.append(order)
            return orders
        except:
            return None

    def get_order_info(self, order_id):
        try:
            id, amount, deal_amount, status, price, type = 0, 0, 0, 0, 0, 0
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                res = HuobiService.getOrderInfo(self.coinType, order_id, CNY_MARKET, ORDER_INFO)
                id = res['id']
                amount = float(res['order_amount'])
                deal_amount = float(res['processed_amount'])
                status = ORDER_STATE_PENDING
                price = float(res['order_price'])
                if res['type'] == 1:
                    type = ORDER_TYPE_BUY
                elif res['type'] == 2:
                    type = ORDER_TYPE_SELL

            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                res = HuobiServiceETH.order_info(order_id)
                id = res['data']['id']
                amount = res['data']['amount']
                deal_amount = res['data']['field-amount']
                state = res['data']['state']
                if state is 'submitted' or state is 'partial-filled':
                    status = ORDER_STATE_PENDING
                elif state is 'canceled':
                    status = ORDER_STATE_CANCELED
                elif state is 'filled':
                    status = ORDER_STATE_CLOSED
                if res['data']['type'] is "buy-market" or res['data']['type'] is "buy-limit":
                    type = ORDER_TYPE_BUY
                elif res['data']['type'] is "sell-market" or res['data']['type'] is "sell-limit":
                    type = ORDER_TYPE_SELL

            order = Order(id, amount, price, deal_amount, status, type)
            return order
        except:
            return None

    def sell(self, price, amount, limit=True):
        try:
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                if limit is True:
                    res = HuobiService.sell(self.coinType, price, amount, None, None, CNY_MARKET, SELL)
                    if res['result'] == "success":
                        return res['id']
                    else:
                        return None
                else:
                    res = HuobiService.sellMarket(self.coinType, amount, None, None, CNY_MARKET, SELL_MARKET)
                    if res['result'] == "success":
                        return res['id']
                    else:
                        return None

            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                if limit is True:
                    res = HuobiServiceETH.orders(amount, 'api', self.coinType, 'sell-limit', price)
                    if res['status'] == "ok":
                        order_id = res['data']
                    else:
                        return None
                    res = HuobiServiceETH.place_order(order_id)
                    if res['status'] == "ok":
                        return order_id
                    else:
                        return None
                else:
                    res = HuobiServiceETH.orders(amount, 'api', self.coinType, 'sell-market')
                    if res['status'] == "ok":
                        order_id = res['data']
                    else:
                        return None
                    res = HuobiServiceETH.place_order(order_id)
                    if res['status'] == "ok":
                        return order_id
                    else:
                        return None
        except:
            return None

    def buy(self, price, amount, limit=True):
        try:
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                if limit is True:
                    res = HuobiService.buy(self.coinType, price, amount, None, None, CNY_MARKET, BUY)
                    if res['result'] == "success":
                        return res['id']
                    else:
                        return None
                elif limit is False:
                    res = HuobiService.buyMarket(self.coinType, amount, None, None, CNY_MARKET, BUY_MARKET)
                    if res['result'] == "success":
                        return res['id']
                    else:
                        return None

            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                if limit is True:
                    res = HuobiServiceETH.orders(amount, 'api', self.coinType, 'buy-limit', price)
                    if res['status'] == "ok":
                        order_id = res['data']
                    else:
                        return None
                    res = HuobiServiceETH.place_order(order_id)
                    if res['status'] == "ok":
                        return order_id
                    else:
                        return None
                else:
                    res = HuobiServiceETH.orders(amount, 'api', self.coinType, 'buy-market')
                    if res['status'] == "ok":
                        order_id = res['data']
                    else:
                        return None
                    res = HuobiServiceETH.place_order(order_id)
                    if res['status'] == "ok":
                        return order_id
                    else:
                        return None
        except:
            return None

    def cancel_order(self, order_id):
        try:
            if self.subject == CNY_BTC or self.subject == CNY_LTC:
                res = HuobiService.cancelOrder(self.coinType, order_id, CNY_MARKET, CANCEL_ORDER)
                if res['result'] == 'success':
                    return True
                else:
                    return False
            if self.subject == CNY_ETH or self.subject == CNY_ETC:
                res = HuobiServiceETH.cancel_order(order_id)
                if res['data'] == 'ok':
                    return True
                else:
                    return False
        except:
            return False

    def cancel_all(self):
        try:
            order_ids = self.get_orders()
            if order_ids:
                for order_id in order_ids:
                    self.cancel_order(order_id.Id)
            return True
        except:
            return False

    def get_rate(self):
        pass



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

    id = exchange.buy(1, 0.01)
    print(exchange.get_order_info(id))
    exchange.cancel_all()
    orders = exchange.get_orders()






