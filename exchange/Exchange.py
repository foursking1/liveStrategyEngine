__author__ = 'foursking'


class Exchange(object):

    def switch_subject(self, subject):
        raise NotImplementedError

    def get_account(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_rate(self):
        raise NotImplementedError

    def get_currency(self):
        raise NotImplementedError

    def get_ticker(self):
        raise NotImplementedError

    def get_depth(self):
        raise NotImplementedError

    def set_precision(self):
        raise NotImplementedError

    def get_records(self):
        raise NotImplementedError

    def buy(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError

    def cancel_order(self):
        raise NotImplementedError

    def get_min_stock(self):
        raise NotImplementedError

    def get_min_price(self):
        raise NotImplementedError






