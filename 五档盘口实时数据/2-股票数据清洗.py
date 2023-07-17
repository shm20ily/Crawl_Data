# name,open,pre_close,price,high,low,bid,ask,volume,amount,b1_v,b1_p,b2_v,b2_p,b3_v,b3_p,b4_v,b4_p,b5_v,b5_p,a1_v,
# a1_p,a2_v,a2_p,a3_v,a3_p,a4_v,a4_p,a5_v,a5_p,date,time,code
import pandas as pd

drop = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount', 'code']
col = ['买①委差', '买①委比', '买②委差', '买②委比', '买③委差', '买③委比', '买④委差', '买④委比', '买⑤委差', '买⑤委比', '卖①委差', '卖①委比', '卖②委差', '卖②委比',
       '卖③委差', '卖③委比', '卖④委差', '卖④委比', '卖⑤委差', '卖⑤委比', 'date', 'time']
df = pd.read_csv('sh_data.csv')
df.drop(columns=drop, inplace=True)
df.columns = col
df.reset_index(drop=True, inplace=True)

# 交换多列
cols = ['date', 'time', '买①委差', '买①委比', '买②委差', '买②委比', '买③委差', '买③委比', '买④委差', '买④委比', '买⑤委差', '买⑤委比', '卖①委差', '卖①委比',
        '卖②委差', '卖②委比', '卖③委差', '卖③委比', '卖④委差', '卖④委比', '卖⑤委差', '卖⑤委比']
df = df.loc[:, cols]
df = df.set_index(['date', 'time'])
df.columns.name = '五档盘口'
# pd.set_option('display.max_columns', None)
print(df)
df.to_csv('SH_600835.csv')
