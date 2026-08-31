import argparse
from pydoc import locate

from libraries.strategy_tester import StrategyTester
from libraries.entities.day_values import DayValues
from libraries.entities.trade import Trade

init_cash = 10000
current_asset = 0

schema = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description='''Framework to test trading strategies.
The program will go through the provided file with historical data on format:
    - CSV file with at least date, open price, close price, columns.
      Take a look at the schema dict to see how the columns must be ordered.
    - The file can have the data on a any specific data frame, 1D, 4h, 1h ...
For each row it will run the implemented strategy.
An empty strategy to be used as super class for the strategy implementation is provided.
No strategy implementation is provided you should implement your strategy or strategies.
The filename, asset (btc, xau, ...), module_name (where the strategy is implemented) 
and strategy_class_name (The implemented strategy class name to test) must to be provided.
if no initial_cash is provided 10000$ will be used.
''',
                    epilog='Text at the bottom of help')
    parser.add_argument('-f', '--filename', type=str, required=True)
    parser.add_argument('-a', '--asset', type=str, required=True)
    parser.add_argument('-m', '--module_name', type=str, required=True)
    parser.add_argument('-s', '--strategy_class_name', type=str, required=True)
    parser.add_argument('-c', '--initial_cash', type=int)
    parser.print_help()
    args = parser.parse_args()

    class_path = f"libraries.strategy.{args.module_name}.{args.strategy_class_name}"
    cls = locate(class_path)
    current_cash = args.initial_cash if args.initial_cash != None else init_cash
    current_strategy = cls(current_asset, int(current_cash), args.asset)

    tester = StrategyTester(args.filename, current_strategy, schema)
    tester.test_strategy()