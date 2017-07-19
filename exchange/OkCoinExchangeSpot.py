__author__ = 'foursking'
from exchange.Exchange import Exchange
from exchange.subject import *
from exchangeConnection.okcoin.util import *
from trade.Account import Account
from trade.Ticker import Ticker
from trade.Depth import Depth
from trade.MarketOrder import MarketOrder
from trade.Order import *
from trade.Trade import *
from exchange.config import *


class OkCoinExchangeSpot(Exchange):

    subject = CNY_BTC
    platform = "okcoin"
    label = "default"
    coinType = OKCOIN_COIN_TYPE_BTC

    def __init__(self):
        self.okcoinSpot = getOkcoinSpot()

    def set_label(self, label):
        self.label = label

    def switch_subject(self, subject):
        if subject == CNY_BTC:
            self.coinType = OKCOIN_COIN_TYPE_BTC
        elif subject == CNY_LTC:
            self.coinType = OKCOIN_COIN_TYPE_LTC
        elif subject == CNY_ETH:
            self.coinType = OKCOIN_COIN_TYPE_ETH
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
            res = self.okcoinSpot.userInfo()
            if self.subject == CNY_BTC:
                balance = float(res['info']['free']['cny'])
                stocks = float(res['info']['free']['btc'])
                frozenBalance = float(res['info']['freezed']['cny'])
                frozenStocks = float(res['info']['freezed']['btc'])

            elif self.subject == CNY_LTC:
                balance = float(res['info']['free']['cny'])
                stocks = float(res['info']['free']['ltc'])
                frozenBalance = float(res['info']['freezed']['cny'])
                frozenStocks = float(res['info']['freezed']['ltc'])

            elif self.subject == CNY_ETH:
                balance = float(res['info']['free']['cny'])
                stocks = float(res['info']['free']['eth'])
                frozenBalance = float(res['info']['freezed']['cny'])
                frozenStocks = float(res['info']['freezed']['eth'])

            account = Account(balance, stocks, frozenBalance, frozenStocks)
            if res['result'] is True:
                return account
            else:
                return None
        except:
            return None

    def get_ticker(self):
        try:
            res = self.okcoinSpot.ticker(self.coinType)
            buy = res['ticker']['buy']
            sell = res['ticker']['sell']
            high = res['ticker']['high']
            low = res['ticker']['low']
            volume = res['ticker']['vol']
            open = 0
            last = res['ticker']['last']
            ticker = Ticker(buy, sell, high, low, volume, open, last)
            return ticker
        except:
            return None

    def get_depth(self, depth_size=5):
        try:
            bids = []
            asks = []
            res = self.okcoinSpot.depth(self.coinType, depth_size)
            for bids in res['bids']:
                price, amount = float(bids[0]), float(bids[1])
                market_order = MarketOrder(price, amount)
                bids.append(market_order)
            for asks in res['asks']:
                price, amount = float(asks[0]), float(asks[1])
                market_order = MarketOrder(price, amount)
                asks.append(market_order)

            depth = Depth(bids, asks)
            return depth
        except:
            return None

    def get_trades(self):
        try:
            trades = []
            res = self.okcoinSpot.trade(self.coinType)
            for item in res:
                time_ms = item['date_ms']
                amount = item['amount']
                price = item['price']
                if item['type'] is "sell":
                    trade_type = TRADE_TYPE_SELL
                elif item['type'] is "buy":
                    trade_type = TRADE_TYPE_BUY
                else:
                    trade_type = TRADE_TYPE_UNDEFINED
                trade = Trade(time_ms, amount, price, trade_type)
                trades.append(trade)
            return trades
        except:
            return None

    def get_orders(self):
        # status:-1:已撤销  0:未成交  1:部分成交  2:完全成交 4:撤单处理中
        try:
            orders = []
            res = self.okcoinSpot.orderInfo(self.coinType, -1)
            if res['result'] is True:
                for item in res['orders']:
                    amount = item['amount']
                    avg_price = item['avg_price']
                    deal_amount = item['deal_amount']
                    order_id = item['order_id']
                    price = item['price']
                    state = item['status']

                    if state == "-1":
                        status = ORDER_STATE_CANCELED
                    elif state == "0" or state == "1":
                        status =  ORDER_STATE_PENDING
                    elif state == "2" or state == "4":
                        status = ORDER_STATE_CLOSED
                    else:
                        status = ORDER_STATE_UNDEFINED

                    raw_order_type = item['type']
                    if raw_order_type == "buy_market" or raw_order_type == "buy":
                        order_type = ORDER_TYPE_BUY
                    else:
                        order_type = ORDER_TYPE_SELL

                    order = Order(order_id, amount, price, deal_amount, status, order_type, avg_price)
                    orders.append(order)
                    return orders
            else:
                return None
        except:
            return None

    def get_order_info(self, order_id):
        try:
            res = self.okcoinSpot.orderInfo(self.coinType, order_id)
            if res['result'] is True:
                for item in res['orders']:
                    amount = item['amount']
                    avg_price = item['avg_price']
                    deal_amount = item['deal_amount']
                    order_id = item['order_id']
                    price = item['price']
                    state = item['status']

                    if state == "-1":
                        status = ORDER_STATE_CANCELED
                    elif state == "0" or state == "1":
                        status =  ORDER_STATE_PENDING
                    elif state == "2" or state == "4":
                        status = ORDER_STATE_CLOSED
                    else:
                        status = ORDER_STATE_UNDEFINED

                    raw_order_type = item['type']
                    if raw_order_type == "buy_market" or raw_order_type == "buy":
                        order_type = ORDER_TYPE_BUY
                    else:
                        order_type = ORDER_TYPE_SELL

                    order = Order(order_id, amount, price, deal_amount, status, order_type, avg_price)
                    return order
            else:
                return None
        except:
            return None

    def buy(self, price, amount, limit=True):
        try:
            if limit is True:
                res = self.okcoinSpot.trade(self.coinType, 'buy', str(price), str(amount))
                if res['result'] is True:
                    return res['order_id']
                else:
                    return None
            else:
                res = self.okcoinSpot.trade(self.coinType, 'buy_market', str(amount))
                if res['result'] is True:
                    return res['order_id']
                else:
                    return None
        except:
            return None

    def sell(self, price, amount, limit=True):
        try:
            if limit is True:
                res = self.okcoinSpot.trade(self.coinType, 'sell', str(price), str(amount))
                if res['result'] is True:
                    return res['order_id']
                else:
                    return None
            else:
                res = self.okcoinSpot.trade(self.coinType, 'sell_market', str(amount))
                if res['result'] is True:
                    return res['order_id']
                else:
                    return None
        except:
            return None

    def cancel_order(self, order_id):
        try:
            res = self.okcoinSpot.cancelOrder(self.coinType, order_id)
            if res['result'] is True:
                return res['order_id']
            else:
                return None
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
