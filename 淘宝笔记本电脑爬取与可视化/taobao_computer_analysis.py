import pandas as pd
import numpy as np
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image


def computer_price():
    """笔记本电脑的价格分布"""
    df = pd.read_excel('taobao_data_笔记本电脑.xlsx')
    price = df['售价']
    sections = [0, 2500, 5000, 7500, 10000, 12500, 15000, 100000]
    group_names = ['2500以下', '2500-5000', '5000-7500', '7500-10000', '10000-12500', '12500-15000', '15000以上']
    cuts = pd.cut(np.array(price), sections, labels=group_names)
    price_counts = pd.value_counts(cuts)
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px', bg_color='white'))
    pie.add(
        '', [list(z) for z in zip([gen for gen in price_counts.index], price_counts)],
        radius=['0', '60%'], center=['50%', '50%'],
        itemstyle_opts=opts.ItemStyleOpts(border_width=2, border_color='white'),
    ).set_series_opts(
        label_opts=opts.LabelOpts(formatter="{d}%", position='top'),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title='笔记本电脑价格区间分布', pos_left='300', pos_top='40',
                                  title_textstyle_opts=opts.TextStyleOpts(color='blue', font_size=20)),
        legend_opts=opts.LegendOpts(pos_right=20, pos_top=250, orient='vertical')
    ).set_colors(
        ['rgba(0, 0, 255, {a})'.format(a=0.9 - 0.1 * x) for x in range(len(group_names))]
    ).render('computer_price_counts.html')


def computer_sales_num():
    """笔记本电脑的购买人数"""
    df = pd.read_excel('taobao_data_笔记本电脑.xlsx')
    sales_num = df['付款人数'].apply(lambda x: int(re.findall(r'\d+', x)[0]))
    sections = [-1, 49, 99, 199, 499, 999, 100000]
    group_names = ['50以下', '50-100', '100-200', '200-500', '500-1000', '1000以上']
    cuts = pd.cut(np.array(sales_num), sections, labels=group_names)
    sales_num_counts = pd.value_counts(cuts)
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px', bg_color='white'))
    pie.add(
        '', [list(z) for z in zip([gen for gen in sales_num_counts.index], sales_num_counts)],
        radius=['30%', '60%'], center=['50%', '50%'],
        itemstyle_opts=opts.ItemStyleOpts(border_width=2, border_color='white'),
    ).set_series_opts(
        label_opts=opts.LabelOpts(formatter="{c}", position='top'),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title='笔记本电脑购买人数分布', pos_left='300', pos_top='40',
                                  title_textstyle_opts=opts.TextStyleOpts(color='rgba(60, 120, 60)', font_size=20)),
        legend_opts=opts.LegendOpts(pos_right=30, pos_top=250, orient='vertical')
    ).set_colors(
        ['rgba(60, 120, 60, {a})'.format(a=0.9 - 0.1 * x) for x in range(len(group_names))]
    ).render('computer_sales_num_counts.html')


def computer_sales500_price():
    """购买人数超过500的笔记本电脑价格分布"""
    df = pd.read_excel('taobao_data_笔记本电脑.xlsx')
    df['人数'] = df['付款人数'].apply(lambda x: int(re.findall(r'\d+', x)[0]))
    sales500_price = df.loc[df['人数'] >= 500, '售价']
    sections = [0, 2500, 5000, 7500, 10000, 100000]
    group_names = ['2500以下', '2500-5000', '5000-7500', '7500-10000', '10000以上']
    cuts = pd.cut(np.array(sales500_price), sections, labels=group_names)
    price_counts = pd.value_counts(cuts)
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px', bg_color='white'))
    pie.add(
        '', [list(z) for z in zip([gen for gen in price_counts.index], price_counts)],
        radius=['0', '60%'], center=['50%', '50%'],
        itemstyle_opts=opts.ItemStyleOpts(border_width=2, border_color='white'),
    ).set_series_opts(
        label_opts=opts.LabelOpts(formatter="{c}款:{d}%", position='top'),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title='购买人数500以上的笔记本电脑价格分布', pos_left='250', pos_top='40',
                                  title_textstyle_opts=opts.TextStyleOpts(color='blue', font_size=20)),
        legend_opts=opts.LegendOpts(pos_right=10, pos_top=250, orient='vertical')
    ).set_colors(
        ['rgba(0, 0, 255, {a})'.format(a=0.9 - 0.1 * x) for x in range(len(group_names))]
    ).render('computer_sales500_price_counts.html')


def computer_sales500_price_Top20():
    """购买人数超过500的笔记本电脑价格Top20"""
    df = pd.read_excel('taobao_data_笔记本电脑.xlsx')
    df['人数'] = df['付款人数'].apply(lambda x: int(re.findall(r'\d+', x)[0]))
    sales500_price = df.loc[df['人数'] >= 500, '售价']
    sales500_price_top20 = sales500_price.sort_values(ascending=False)[0: 20]
    sales500_price_top20_shop = df.loc[sales500_price_top20.index, '店铺名']
    bar = Bar(init_opts=opts.InitOpts(width='1000px', height='400px', bg_color='white'))
    bar.add_xaxis(
        sales500_price_top20_shop.to_list()
    ).add_yaxis(
        '', sales500_price_top20.to_list(), category_gap=20
    ).set_global_opts(
        title_opts=opts.TitleOpts(title='购买人数超过500的笔记本电单价Top20', pos_left='350', pos_top='30',
                                  title_textstyle_opts=opts.TextStyleOpts(color='#4863C4', font_size=16)),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10, rotate=25, color='#4863C4'))
    ).set_colors('#4863C4').render('computer_sales500_price_top20.html')


def computer_title_word_cloud():
    """笔记本电脑的标题词云"""
    df = pd.read_excel('taobao_data_笔记本电脑.xlsx')
    title_content = df['标题']
    all_word = ','.join([str(t) for t in title_content])
    cut_text = jieba.cut(all_word)
    result = ' '.join(cut_text)
    pic = Image.open("computer.png")
    shape = np.array(pic)
    exclude = {'代'}
    image_colors = ImageColorGenerator(shape)
    wc = WordCloud(font_path="simhei.ttf", width=800, height=600, max_words=800, max_font_size=80, min_font_size=5,
                   background_color='white', color_func=image_colors,
                   contour_width=3, contour_color='steelblue', stopwords=exclude,
                   prefer_horizontal=1, mask=shape, relative_scaling=0.5)
    wc.generate(result)
    wc.to_file("ciyun_computer_title.png")


if __name__ == '__main__':
    computer_price()
    computer_sales_num()
    computer_sales500_price()
    computer_sales500_price_Top20()
    computer_title_word_cloud()
