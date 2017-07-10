#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'foursking'

class Depth(object):

    Bids = []
    Asks = []

    def __str__(self):
        bids_length = len(self.Bids)
        asks_length = len(self.Asks)

        bids_str = "买盘深度 %d " % bids_length
        asks_str = "卖盘深度 %d " % asks_length
        for index, bids in enumerate(self.Bids):
            bids_str += ",买 %d, %s" % (index+1, bids)
        for index, asks in enumerate(self.Asks):
            asks_str += ",买 %d, %s" % (index+1, asks)
        return bids_str + "\n" + asks_str
