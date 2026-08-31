class Strategy(object):
    def __init__(self, current_asset=None, current_cash=None, asset=None):
      self.current_asset = current_asset
      self.current_cash = current_cash
      self.asset = asset
      self.bought = False
      self.trades = []

    def get_trades(self):
      return self.trades

    def did_buy(self):
      return self.bought

    def get_current_cash(self):
      return self.current_cash

    def get_current_asset(self):
      return self.current_asset

    def run_strategy(self, all_data):
      pass