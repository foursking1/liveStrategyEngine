from exchange.Exchange import Exchange

def initialize(context):
    pass

def handle_data(context):
    exchanges = context.exchanges
    for e in exchanges:
        #assert isinstance(e, Exchange)
        e.get_account()





