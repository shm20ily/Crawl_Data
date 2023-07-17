import pandas as pd
from pyecharts.commons.utils import JsCode
from pyecharts.charts import *
from pyecharts import options as opts

data = pd.read_csv('去哪儿.csv')
data.info()
data = data[~data['地点'].isin(['攻略'])]
data = data[~data['天数'].isin(['99+'])]
data
data.drop_duplicates(inplace=True)
data['人均费用'].fillna(0, inplace=True)
data['人物'].fillna('独自一人', inplace=True)
data['玩法'].fillna('没有', inplace=True)
data['天数'] = data['天数'].astype(int)
data = data[data['人均费用'].values > 200]
data = data[data['天数'] <= 15]
data
data = data.reset_index(drop=True)
data


def Month(e):
    m = str(e).split('/')[2]
    if m == '01':
        return '一月'
    if m == '02':
        return '二月'
    if m == '03':
        return '三月'
    if m == '04':
        return '四月'
    if m == '05':
        return '五月'
    if m == '06':
        return '六月'
    if m == '07':
        return '七月'
    if m == '08':
        return '八月'
    if m == '09':
        return '九月'
    if m == '10':
        return '十月'
    if m == '11':
        return '十一月'
    if m == '12':
        return '十二月'


data['旅行月份'] = data['出发时间'].apply(Month)
data['出发时间'] = pd.to_datetime(data['出发时间'])
data
import re


def Look(e):
    if '万' in e:
        num1 = re.findall('(.*?)万', e)
        return float(num1[0]) * 10000
    else:
        return float(e)


data['浏览次数'] = data['浏览量'].apply(Look)
data.drop(['浏览量'], axis=1, inplace=True)
data['浏览次数'] = data['浏览次数'].astype(int)
data.head()
data1 = data
data1['地点'].value_counts().head(10)
loc = data1['地点'].value_counts().head(10).index.tolist()
print(loc)
loc_data = data1[data1['地点'].isin(loc)]
price_mean = round(loc_data['人均费用'].groupby(loc_data['地点']).mean(), 1)
print(price_mean)
price_mean2 = [1630.1, 1862.9, 1697.9, 1743.4, 1482.4, 1586.4, 1897.0, 1267.5, 1973.8, 1723.7]


m2 = data1['地点'].value_counts().head(10).index.tolist()
n2 = data1['地点'].value_counts().head(10).values.tolist()
bar = (
    Bar(init_opts=opts.InitOpts(height='500px', width='1000px', theme='dark'))
    .add_xaxis(m2)
    .add_yaxis(
        '目的地Top10',
        n2,
        label_opts=opts.LabelOpts(is_show=True, position='top'),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode("""new echarts.graphic.LinearGradient(
            0, 0, 0, 1,[{offset: 0,color: 'rgb(255,99,71)'}, {offset: 1,color: 'rgb(32,178,170)'}])
            """
                         )
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='目的地Top10'),
        xaxis_opts=opts.AxisOpts(name='景点名称',
                                 type_='category',
                                 axislabel_opts=opts.LabelOpts(rotate=90),
                                 ),
        yaxis_opts=opts.AxisOpts(
            name='数量',
            min_=0,
            max_=120.0,
            splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(type_='dash'))
        ),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
    )

    .set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_='average', name='均值'),
                opts.MarkLineItem(type_='max', name='最大值'),
                opts.MarkLineItem(type_='min', name='最小值'),
            ]
        )
    )
)
bar.render_notebook()

bar = (
    Bar(init_opts=opts.InitOpts(height='500px', width='1000px', theme='dark'))
    .add_xaxis(loc)
    .add_yaxis(
        '人均费用',
        price_mean2,
        label_opts=opts.LabelOpts(is_show=True, position='top'),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode("""new echarts.graphic.LinearGradient(
            0, 0, 0, 1,[{offset: 0,color: 'rgb(255,99,71)'}, {offset: 1,color: 'rgb(32,178,170)'}])
            """
                         )
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='各景点人均费用'),
        xaxis_opts=opts.AxisOpts(name='景点名称',
                                 type_='category',
                                 axislabel_opts=opts.LabelOpts(rotate=90),
                                 ),
        yaxis_opts=opts.AxisOpts(
            name='数量',
            min_=0,
            max_=2000.0,
            splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(type_='dash'))
        ),
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
    )

    .set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_='average', name='均值'),
                opts.MarkLineItem(type_='max', name='最大值'),
                opts.MarkLineItem(type_='min', name='最小值'),
            ]
        )
    )
)
bar.render_notebook()
data1['天数'].value_counts()
data1['旅行时长'] = data1['天数'].apply(lambda x: str(x) + '天')
data1
data1['人物'].value_counts()
m = data1['浏览次数'].sort_values(ascending=False).index[:].tolist()
data1 = data1.loc[m]
data1 = data1.reset_index(drop=True)
data1
data1['旅行月份'].value_counts()
word_list = []
for i in data1['玩法']:
    s = re.split('\xa0', i)
    word_list.append(s)
dict = {}
for j in range(len(word_list)):
    for i in word_list[j]:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1
# print(dict)
list = []
for item in dict.items():
    list.append(item)
for i in range(1, len(list)):
    for j in range(0, len(list) - 1):
        if list[j][1] < list[j + 1][1]:
            list[j], list[j + 1] = list[j + 1], list[j]
print(list)

data1['旅行月份'].value_counts()
m1 = data1['人物'].value_counts().index.tolist()
n1 = data1['人物'].value_counts().values.tolist()
pie = (Pie(init_opts=opts.InitOpts(theme='dark', width='1000px', height='800px'))
       .add("", [z for z in zip(m1, n1)],
            radius=["40%", "65%"])
       .set_global_opts(title_opts=opts.TitleOpts(title="去哪儿\n\n出游结伴方式", pos_left='center', pos_top='center',
                                                  title_textstyle_opts=opts.TextStyleOpts(
                                                      color='#FF6A6A', font_size=30, font_weight='bold'),
                                                  ),
                        visualmap_opts=opts.VisualMapOpts(is_show=False,
                                                          min_=38,
                                                          max_=641,
                                                          is_piecewise=False,
                                                          dimension=0,
                                                          range_color=['#9400D3', '#008afb', '#ffec4a', '#FFA500',
                                                                       '#ce5777']),
                        legend_opts=opts.LegendOpts(is_show=False, pos_top='5%'),
                        )
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=12),
                        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c}"),
                        itemstyle_opts={"normal": {
                            "barBorderRadius": [30, 30, 30, 30],
                            'shadowBlur': 10,
                            'shadowColor': 'rgba(0,191,255,0.5)',
                            'shadowOffsetY': 1,
                            'opacity': 0.8
                        }
                        })

       )
pie.render_notebook()

m3 = data1['出发时间'].value_counts().sort_index()[:]
m4 = m3['2021'].index
n4 = m3['2021'].values
m3['2021'].sort_values().tail(10)
line = (
    Line()
    .add_xaxis(m4.tolist())
    .add_yaxis('', n4.tolist())
)
line.render_notebook()
m5 = []
n5 = []
for i in range(20):
    m5.append(list[i][0])
    n5.append(list[i][1])
m5.reverse()
m6 = m5
n5.reverse()
n6 = n5

bar = (
    Bar(init_opts=opts.InitOpts(theme='dark', width='1000px', height='500px'))
    .add_xaxis(m6)
    .add_yaxis('', n6)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True,
                                               position='insideRight',
                                               font_style='italic'),
                     itemstyle_opts=opts.ItemStyleOpts(
                         color=JsCode("""new echarts.graphic.LinearGradient(1, 0, 0, 0, 
                                             [{
                                                 offset: 0,
                                                 color: 'rgb(255,99,71)'
                                             }, {
                                                 offset: 1,
                                                 color: 'rgb(32,178,170)'
                                             }])"""))
                     )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="出游玩法分析"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        legend_opts=opts.LegendOpts(is_show=True))
    .reversal_axis()
)
bar.render_notebook()
m7 = data1['旅行时长'].value_counts().index.tolist()
n7 = data1['旅行时长'].value_counts().values.tolist()
data_day = data1['旅行时长'].value_counts().sort_values()
bar = (
    Bar(init_opts=opts.InitOpts(theme='dark', width='1000px', height='500px'))
    .add_xaxis(data_day.index.tolist())
    .add_yaxis('', data_day.values.tolist())
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True,
                                               position='insideRight',
                                               font_style='italic'),
                     itemstyle_opts=opts.ItemStyleOpts(
                         color=JsCode("""new echarts.graphic.LinearGradient(1, 0, 0, 0, 
                                             [{
                                                 offset: 0,
                                                 color: 'rgb(255,99,71)'
                                             }, {
                                                 offset: 1,
                                                 color: 'rgb(32,178,170)'
                                             }])"""))
                     )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="旅行时长"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        legend_opts=opts.LegendOpts(is_show=True))
    .reversal_axis()
)
bar.render_notebook()
data_mo = data1[((data1['旅行月份'] == '七月') | (data1['旅行月份'] == '八月')) & (data1['人物'] == '三五好友')].drop(
    ['旅行时长'], axis=1)
data_mo.head(10)
data_mo2 = data1[((data1['人物'] == '情侣') | (data1['人物'] == '独自一人')) & (data1['旅行月份'] == '十月')].drop(
    ['旅行时长'], axis=1)
data_mo2.head(10)

import jieba
import jieba.analyse
import re

punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}【】'


def remove_fuhao(e):
    short = re.sub(r"[%s]+" % punc, " ", e)
    return short


def cut_word(text):
    text = jieba.cut_for_search(str(text))
    return ' '.join(text)


data2 = data1
data2['简介'] = data2['短评'].apply(remove_fuhao).apply(cut_word)
data2.head()
word = data2['简介'].values.tolist()
fb = open(r'.\travel_text.txt', 'w', encoding='utf-8')
for i in range(len(word)):
    fb.write(word[i])
with open(r'.\travel_text.txt', 'r', encoding='utf-8') as f:
    words = f.read()
    f.close
jieba.analyse.set_stop_words(r'./stopwords.txt')
new_words = jieba.analyse.textrank(words, topK=30, withWeight=True)
print(new_words)
word1 = []
num1 = []
for i in range(len(new_words)):
    word1.append(new_words[i][0])
    num1.append(new_words[i][1])
    wordcloud = (
        WordCloud()
        .add('简介词云分析', [z for z in zip(word1, num1)], word_size_range=[25, 80], shape='diamond')
    )
    wordcloud.render_notebook()
data4 = data1.drop(['旅行时长', '简介'], axis=1)
data4
k_list = []
the_list = []
keyword = input('请输入旅行月份：')
data5 = data4[data4['旅行月份'] == str(keyword)]
keyword1 = input('请输入结伴出游方式：')
data6 = data5[data5['人物'] == str(keyword1)]
price = int(input('请输入预期价格上限：'))
data7 = data6[data6['人均费用'] <= price]
day1 = int(input('请输入旅行时长下限：'))
day2 = int(input('请输入旅行时长上限：'))
data8 = data7[(data7['天数'] >= day1) & (data7['天数'] <= day2)]
data8
