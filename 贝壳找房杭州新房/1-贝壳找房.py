import requests
from bs4 import BeautifulSoup
import csv

data_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 '
                  'Safari/537.36 SLBrowser/8.0.0.5261 SLBChan/103'
}
total_pages = 92


def get_html(url, headers):
    html = requests.get(url, headers=headers).content.decode('utf-8')
    return html


def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    for div in soup.find_all('div', class_="resblock-desc-wrapper"):
        for n, div_tag in enumerate(div.find_all('div', class_='resblock-name')):
            item = {}
            name = div_tag.find('a')
            # print(name['href'])
            span_list = div_tag.find('span')

            if n == 0:
                item['楼盘链接'] = ("".join(name['href']))
                item["楼盘名称"] = ("".join(name.stripped_strings))
                item["楼盘状态"] = ("".join(span_list.stripped_strings))
            else:
                item['楼盘链接'] = ("".join(name['href']))
                item["楼盘名称"] = ("".join(name.stripped_strings))
                item["楼盘状态"] = ("".join(span_list.stripped_strings))

            print(item)
            data_list.append(item)


def save_data():
    with open('beike_test.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ["楼盘链接", "楼盘名称", "楼盘状态"])
        writer.writeheader()
        writer.writerows(data_list)


def main():
    url = 'http://hz.fang.ke.com/loupan/pg{}/'
    for page in range(1, total_pages + 1):
        # print(page)
        # 构建完整的url
        url_p = url.format(page)
        # print(url_p)
        html = get_html(url_p, headers)
        get_data(html)
        # print(html)
        save_data()


main()
