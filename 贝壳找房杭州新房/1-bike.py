import requests
import csv
import pandas as pd
from lxml import etree

df = pd.read_csv('beike.csv')
# df = df['楼盘链接'].values[451: 901]
df = df['楼盘链接'].values[1351:]

data_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 '
                  'Safari/537.36 SLBrowser/8.0.0.5261 SLBChan/103'
}


def get_data(url_lp):
    response = requests.get(url_lp, headers=headers)
    html = etree.HTML(response.content.decode('utf-8'))
    # print(html)

    # 匹配到所有的li节点
    obj = html.xpath('//li[1]')
    # print(obj)

    for li in obj[0]:
        item = {}
        item["楼盘性质"] = li.xpath('//ul[@class="x-box"][1]/li[1]/span[position()=2]/text()')[0]
        item["楼盘单价"] = li.xpath('//ul[@class="x-box"][1]/li[2]/span[2]/span/text()')[0]
        item["开发商名"] = li.xpath('//ul[@class="x-box"][1]/li[7]/span[2]/text()')[0]
        print(item)
        data_list.append(item)


def save_data():
    with open('loupan3.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ["楼盘性质", "楼盘单价", "开发商名"])
        writer.writeheader()
        writer.writerows(data_list)


def main():
    url = 'https://hz.fang.ke.com{}xiangqing/'
    for lp in df:
        url_lp = url.format(lp)
        get_data(url_lp)
        save_data()


main()
