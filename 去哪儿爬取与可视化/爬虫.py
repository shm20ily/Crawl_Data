import random
import time
import requests  # 发送网络请求
import parsel  # 筛选数据模块
import csv  #

csv_qne = open('去哪儿.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_qne)
csv_writer.writerow(['地点', '短评', '出发时间', '天数', '人均费用', '人物', '玩法', '浏览量', '详情页'])
for page in range(1, 201):
    url = f'https://travel.qunar.com/travelbook/list.htm?page={page}&order=hot_heat'
    # 写爬虫 没有太大区别
    # post里面需要加一些请求参数
    # 在网站开发当中 get请求不是很安全的请求 有长度限制的
    # post 更加安全 提交表单数据内容 没有长度限制的
    response = requests.get(url)
    # <Response [200]>: 访问成功了, 接下来我们就只需要拿数据就行了

    html_data = response.text
    selector = parsel.Selector(html_data)
    # css选择器提取网页内容
    # 需要有网页开发基础
    url_list = selector.css('body > div.qn_mainbox > div > div.left_bar > ul > li > h2 > a::attr(href)').getall()
    for detail_url in url_list:
        detail_id = detail_url.replace('/youji/', '')
        detail_url = 'https://travel.qunar.com/travelbook/note/' + detail_id
        response_1 = requests.get(detail_url)
        data_html_1 = response_1.text
        #   出发日期 天数 人均费用 人物 玩法 地点 浏览量...
        selector_1 = parsel.Selector(data_html_1)
        # ::text 提取标签里面文本内容 *所有
        # 标题
        title = selector_1.css('.b_crumb_cont *:nth-child(3)::text').get()
        # 短评
        comment = selector_1.css('.title.white::text').get()
        # 浏览量
        count = selector_1.css('.view_count::text').get()
        # 出发日期
        date = selector_1.css('#js_mainleft > div.b_foreword > ul > li.f_item.when > p > span.data::text').get()
        # 天数
        days = selector_1.css('#js_mainleft > div.b_foreword > ul > li.f_item.howlong > p > span.data::text').get()
        # 人均费用
        money = selector_1.css('#js_mainleft > div.b_foreword > ul > li.f_item.howmuch > p > span.data::text').get()
        # 人物
        character = selector_1.css('#js_mainleft > div.b_foreword > ul > li.f_item.who > p > span.data::text').get()
        # 玩法
        play_list = selector_1.css(
            '#js_mainleft > div.b_foreword > ul > li.f_item.how > p > span.data span::text').getall()
        play = ' '.join(play_list)
        print(title, comment, date, days, money, character, play, count, detail_url)
        csv_writer.writerow([title, comment, date, days, money, character, play, count, detail_url])
        time.sleep(random.randint(3, 5))
csv_qne.close()
