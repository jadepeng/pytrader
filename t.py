import datetime

from easyquant.quotation import use_quotation

quotation = use_quotation('jqdata')
codes = {
    "512580": "碳中和",
    "002233": "塔牌",
    "002230": "讯飞",
    "600036": "招行",
    "601318": "平安",
    "600900": "长电",
    "600048": "保利"}

for stock in codes.keys():
    df = quotation.get_bars(stock, count=200, end_dt=datetime.datetime.now() - datetime.timedelta(days=1))

    last = df[-1:]

    high = last.high[0]
    low = last.low[0]
    close = last.close[0]
    pivot = (high + low + close) / 3

    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    s1 = 2 * pivot - high
    s2 = pivot - (high - low)

    print("%s %s : 阻力价格1 = %s, 阻力价格2 = %s, 支撑1 =%s , 支撑2 =%s" % (codes[stock], stock, r1, r2, s1, s2))

# sSetup = pivot + (high - low)  # 观察卖出价 r2
# sEnter = 2 * pivot - low  # 反转卖出价 r1
# bSetup = pivot - (high - low)  # 观察买入价 s2
# bEnter = 2 * pivot - high  # 反转买入价 s1
#
# print(pivot, sSetup, sEnter, bSetup, bEnter)
