# pytrader

[English README](README_EN.md) | [中文说明](README.md)

A quantitative trading framework based on [easytrader](https://github.com/shidenggui/easytrader) and [easyquotation](https://github.com/shidenggui/easyquotation).

Supports automated trading on Eastmoney (东方财富).

## Maintenance Plan

This project is currently maintained as a personal open-source project. Priority is given to ensuring the usability and compatibility of existing features. There is no commitment to a fixed release cycle.

- Priority is given to fixing actual issues that affect installation, startup, trading execution, and backtesting results.
- Minor and clear bug fixes are preferred. Large-scale refactoring without real-world scenario validation will not be accepted.
- The web frontend and automated trading capabilities will be incrementally maintained based on the existing implementation.
- Breaking changes require explicit migration guidelines.

## Roadmap

- Improve documentation for installation, configuration, backtesting, and online trading.
- Provide sample configuration files to avoid exposing real account credentials in the documentation.
- Streamline strategy templates and backtesting examples to reduce the cost of integrating new strategies.
- Add minimal tests for critical paths, covering configuration loading, strategy loading, and basic backtesting flows.

## Security Boundaries

**Do not submit real broker accounts, passwords, tokens, sessions, market data API keys, or any production credentials.**

- Files like `account.json`, `yjb_account.json`, `jqdata.json`, `tushare.json`, `*.session`, and `*.local` must only be saved locally or in your deployment environment.
- Repository examples must use placeholder values. Never write real account credentials into code, READMEs, issues, or commit histories.
- Before using a real account, you must verify the strategy, risk control, order submission paths, and exception handling in a test environment.
- This project does not host credentials and does not assume any responsibility for broker authentication, fund security, or trading risks.

## Non-Investment Advice Disclaimer

This project only provides engineering code examples related to quantitative trading, market data acquisition, strategy execution, and backtesting. It does not constitute any investment advice, yield commitments, or trading instructions. Users should judge strategy risks independently and bear all losses caused by real-money trading.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. Third-party dependencies and upstream projects retain their respective licenses.

## Installation

```bash
pip3 install -r requirements.txt
```

- Manually install the `talib` dependency, see [TA-Lib Python wrapper](https://github.com/cgohlke/talib-build/releases) or the UCI binary builds archive.

## Web System & API Service

This project provides a companion web frontend and API service for real-time monitoring of stock watchlists and grid trading (T-operation) pricing.

- **Watchlist Monitoring**: Supports adding/removing stocks, with real-time price updates via the QQ quotation API.
- **Automated Trading APIs**: Features secure buy (`/api/buy`) and sell (`/api/sell`) endpoints, fully protected by JWT authorization to ensure trading security.

![Watched Stocks](doc/watch_stock.png)

## Strategy Files

You can write your own strategies in the `strategies` directory by referring to the existing examples.

Strategies must inherit from the `StrategyTemplate` class and implement the `init` and `on_bar` functions.

The `init` function configures the stock watchlist, after which the quotation engine will push market data for those stocks:

```python
    def init(self):
        for stock_code in self.watch_stocks:
            self.quotation_engine.watch(stock_code)
```

When market data arrives, it triggers the `on_bar` function:

```python
def on_bar(self, context: Context, data: Dict[str, DataFrame]):
    pass
```

- `Context` is a utility class for retrieving other bars or calculating technical indicators like CCI, RSI, etc.
- `data` is the pushed market data dictionary. You can retrieve DataFrame-format market data using the stock code.

## Online Trading

See `tradertest.py`. It loads all strategies. You can modify it slightly to support specific strategies.

```python
import easyquant
from easyquant import DefaultLogHandler

print('Test DEMO')

# Broker
broker = 'eastmoney'

# Prepare this locally, do NOT commit real account credentials or tokens
# {
#     "user": "your-broker-user",
#     "password": "your-broker-password"
# }
need_data = 'account.json'

log_type = 'file'

log_handler = DefaultLogHandler(name='Test', log_type=log_type, filepath='logs.log')

m = easyquant.MainEngine(broker,
                         need_data,
                         quotation='online',
                         # 1-minute K-line
                         bar_type="1m",
                         log_handler=log_handler)
m.is_watch_strategy = True  # Automatically reload when strategy files change (not recommended for production)
m.load_strategy()
m.start()
```

## Backtesting

See `backtest.py`. Set the backtesting timeframe and strategy. Note that the quotation source must be `tushare` or `jqdata` (you can apply for your own keys).

```python
import easyquotation

import easyquant
from easyquant import DefaultLogHandler, PushBaseEngine
from easyquant.log_handler.default_handler import MockLogHandler
from strategies.CCI import Strategy

print('Backtest Demo')

broker = 'mock'
need_data = 'account.json'

mock_start_dt = "2020-01-01"
mock_end_dt = "2021-11-11"

m = easyquant.MainEngine(broker, need_data,
                         quotation='tushare',
                         # quotation='jqdata',
                         bar_type="1d")

log_handler = MockLogHandler(context=m.context)

# Choose strategy
strategy = Strategy(user=m.user, log_handler=log_handler, main_engine=m)

m.start_mock(mock_start_dt, mock_end_dt, strategy)

print('mock end')

print(m.user.get_balance())

for deal in m.user.get_current_deal():
    print(deal.deal_time, deal.bs_type, deal.deal_price, deal.deal_amount)
```
