#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'foursking'

ORDER_STATE_PENDING  = 0
ORDER_STATE_CLOSED = 1
ORDER_STATE_CANCELED = 2
ORDER_STATE_UNDEFINED = -1

ORDER_TYPE_BUY  = 0
ORDER_TYPE_SELL = 1


class Order(object):

    Status = 0
    Amount = 0.0
    DealAmount = 0.0
    Price = -1
    Type = 0
    Id = 0
    AvgPrice = 0.0

    def __init__(self, id, amount, price, deal_amount, status, type, avgprice=0.0):
        self.Id = id
        self.Amount = float(amount)
        self.Price = float(price)
        self.DealAmount = float(deal_amount)
        self.Status = int(status)
        self.Type = int(type)
        self.AvgPrice = float(avgprice)

    def __str__(self):
        order_state = ""
        order_type = ""
        if self.Status == ORDER_STATE_CANCELED:
            order_state = "订单取消"
        elif self.Status == ORDER_STATE_CLOSED:
            order_state = "订单关闭"
        elif self.Status == ORDER_STATE_PENDING:
            order_state = "订单未完成"

        if self.Type == ORDER_TYPE_BUY:
            order_type = "买单"
        elif self.Type == ORDER_TYPE_SELL:
            order_type = "卖单"

        return "订单状态 %s， 下单数量 %f， 成交数量 %f， 下单价格 %f， 订单类型 %s， 订单 id %s， 平均成交均价格 %f" % (
            order_state, self.Amount, self.DealAmount, self.Price, order_type, self.Id, self.AvgPrice
        )