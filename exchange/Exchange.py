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

    def buy(self,price, amount, limit):
        raise NotImplementedError

    def sell(self, price, amount, limit):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError

    def get_order_info(self, order_id):
        raise NotImplementedError

    def cancel_order(self, id):
        raise NotImplementedError

    def cancel_all(self):
        raise NotImplementedError

    def get_min_stock(self):
        raise NotImplementedError

    def get_min_price(self):
        raise NotImplementedError






