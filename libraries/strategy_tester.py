from libraries.entities.day_values import DayValues
from libraries.entities.trade import Trade

class StrategyTester():
    def __init__(self, file=None, current_strategy=None, schema={'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}):
      self.file = file
      self.current_strategy = current_strategy
      self.schema = schema
      self.ema50 = []
      self.ema25 = []
      self.all_data = []
      self.check_setup()

    def check_setup(self):
      self.check_file()
      self.check_strategy()
      self.check_schema()

    def check_file(self):
        if self.file == None:
            print("No data file defined, finishing tester")
            exit(0)

    def check_strategy(self):
        if self.current_strategy == None:
            print("No strategy defined, finishing tester")
            exit(0)

    def check_schema(self):
        if 'date' in self.schema and 'open' in self.schema and 'close' in self.schema:
            return
        
        print("The schema must have at least the date, open and close keys, finishing tester")
        exit(0)
      
    def print_summary(self):
        print("=" * 40)
        print(self.ema25)
        print(list(map(str, self.all_data)))
        print(f"current cash {self.current_strategy.get_current_cash()}")
        print(f"current asset {self.current_strategy.get_current_asset()}")
        print(list(map(str, self.current_strategy.get_trades())))
        chars = "=" * 20
        print(f"{chars} Summary end {chars}" )

    def printTrades(self):
        print(list(map(str, self.current_strategy.get_trades())))
        opc = input("Do you want to save the trades to a file? (yes/no): ")
        if opc == "yes":
          file = input("Enter the file name with extension, ex: trades.txt: ")
          with open(file,"w") as out:
            out.write("\n".join(list(map(str, self.current_strategy.get_trades()))))

    def printData(self, opc):
        if "all" in opc:
            print(list(map(str,self.all_data)))
        else:
            last_trades_to_show = opc[-1]
            if last_trades_to_show not in "1,2,3,4,5,6,7,8,9":
                print(str(self.all_data[-1]))
            else:
                print(list(map(str, self.all_data[int(opc[-1]) * - 1:])))

    def printEma25(self):
        print(self.ema25)

    def printEma50(self):
        print(self.ema50)

    def printCash(self):
        print(self.current_strategy.get_current_cash())

    def get_all_data_close_prices(self):
        prices = []
        for dayv in self.all_data:
            prices.append(float(dayv.close_price))
        return prices

    def ema(self, current_price, prev_ema, period = 50):
        multiplier = 2 / (1 + period)
        return (current_price * multiplier) + (prev_ema * (1-multiplier))


    def percentage(self, initial, current):
        diff = initial - current
        return (diff * 100) / initial

    def calculate_metrics(self):
        # if we reach the first day with a complete period a simple ma must be calculated
        period = len(self.all_data)

        if period < 25:
            return
        elif period == 25:
            all_data_close_prices = self.get_all_data_close_prices()
            self.ema25.append(sum(all_data_close_prices)/period)
            emas25 = ",".join(map(str, all_data_close_prices))
        elif period < 50:
            self.ema25.append(self.ema(self.all_data[-1].close_price, self.ema25[-1], 25))
        elif period == 50:
            self.ema25.append(self.ema(self.all_data[-1].close_price, self.ema25[-1], 25))
            all_data_close_prices = self.get_all_data_close_prices()
            self.ema50.append(sum(all_data_close_prices)/period)
            emas50 = ",".join(map(str, all_data_close_prices))
        else:
            self.ema25.append(self.ema(self.all_data[-1].close_price, self.ema25[-1], 25))
            self.ema50.append(self.ema(self.all_data[-1].close_price, self.ema50[-1], 50))

    def process_day(self, day_values):
        # get the line values
        values = day_values.split(',')
        day_values_object = DayValues(
        date = values[self.schema['date']],
        open_price = float(values[self.schema['open']]),
        high_price = float(values[self.schema['high']]),
        low_price = float(values[self.schema['low']]),
        close_price = float(values[self.schema['close']]),
        )
        self.calculate_metrics()
        day_values_object.ema25 = self.ema25[-1] if len(self.ema25) > 0 else 0
        day_values_object.ema50 = self.ema50[-1] if len(self.ema50) > 0 else 0
        self.all_data.append(day_values_object)
        
        print(f"runing strategy on {values[self.schema['date']]}")
        
        self.current_strategy.run_strategy(self.all_data)
        if self.current_strategy.did_buy() == False and self.current_strategy.get_current_cash() <= 100:
            opc = input("we have lost at least 90%: ")
            if opc == "exit":
                exit(0)

    def show_options(self):
        while True:
            opc = input("Enter an option (trades, data, ema25, ema50, cash), exit for finish: ")
            if opc == "exit":
                exit(0)
            elif opc == "trades":
                self.printTrades()
            elif opc[-4:] == "data":
                self.printData(opc)
            elif opc == "ema25":
                self.printEma25()
            elif opc == "ema50":
                self.printEma50()
            elif opc == "cash":
                self.printCash()
            else:
                break
            print("=" * 40)

    def test_strategy(self):
        with open(self.file,'r') as inp:
            headers = True
            # read line by line, each line is one frame time price
            for line in inp.readlines():
                try:
                    if headers:
                        headers = False
                        continue
                    # process a day data
                    self.process_day(line)
                except KeyboardInterrupt:
                    self.show_options()
            self.show_options()
