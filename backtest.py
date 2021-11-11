import easyquotation

import easyquant
from easyquant import  DefaultLogHandler, PushBaseEngine
from easyquant.log_handler.default_handler import MockLogHandler
from strategies.CCI import Strategy

print('backtest 回测 测试 ')

broker = 'mock'
need_data = 'account.json'

#
mock_start_dt = "2020-01-01"
mock_end_dt= "2021-11-11"


m = easyquant.MainEngine(broker, need_data,
                         quotation='tushare',
                         # quotation='jqdata',
                         bar_type="1d")

log_handler = MockLogHandler(context=m.context)

# 选择策略
strategy = Strategy(user=m.user, log_handler=log_handler, main_engine=m)

m.start_mock(mock_start_dt, mock_end_dt, strategy)

print('mock end')

print(m.user.get_balance())

for deal in m.user.get_current_deal():
    print(deal.deal_time, deal.bs_type, deal.deal_price, deal.deal_amount)
