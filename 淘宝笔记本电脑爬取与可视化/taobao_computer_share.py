import requests
import time
import re
import pandas as pd
import json

# user-agent和cookie需要自己准备
headers = {
    "cookie": "",
    'User-Agent': '',
}
# 修改goods可以修改自己想爬的商品
GOODS = '笔记本电脑'
# 修改PAGE可以修改爬的页数
PAGE = 100


def data_parse(html):
    # with open('test.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    title = re.findall(r'\"raw_title\"\:\"(.*?)\"', html)
    # print(title, len(title))
    price = re.findall(r'\"view_price\"\:\"([\d\.]*)\"', html)
    # print(price, len(price))
    sales_num = re.findall(r'\"view_sales\"\:\"(.*?)\"', html)
    # print(sales_num, len(sales_num))
    location = re.findall(r'\"item_loc\"\:\"(.*?)\"', html)
    # print(location, len(location))
    shop_name = re.findall(r'\"shopName\"\:\"(.*?)\"', html)
    # print(shop_name, len(shop_name))
    df_res = pd.DataFrame(
        {"标题": title, "售价": price, "付款人数": sales_num, "店铺位置": location, "店铺名": shop_name}
    )
    return df_res


def get_taobao_data():
    df_data = pd.DataFrame()
    for p in range(PAGE):
        try:
            print("-----开始获取第{}页数据-------".format(p + 1))
            url = 'https://s.taobao.com/search?q={}&s={}'.format(GOODS, 44 * p)
            res = requests.get(url, headers=headers, timeout=30)
            print("---------获取第{}页数据成功---{}".format(p + 1, res.status_code))
            df_res = data_parse(res.text)
            df_data = pd.concat([df_data, df_res])
        except Exception as e:
            time.sleep(10)
            print("---------获取第{}页数据失败---{}".format(p + 1, e))
            continue
        time.sleep(10)
    df_data.to_excel('taobao_data_{}.xlsx'.format(GOODS))


if __name__ == '__main__':
    get_taobao_data()
