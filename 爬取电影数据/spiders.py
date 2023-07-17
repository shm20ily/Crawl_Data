import json
import logging
import random
import urllib
from time import sleep

logging.captureWarnings(True)
import requests
import csv
import os

from lxml import etree
from pymysql import *
import re
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/dbm')
st = 0
List = ['2022', '2021', '2020', '2019', '2010年代', '2000年代', '90年代', '80年代', '70年代', '60年代', '更早']  # 分类列表


class spider(object):
    def __init__(self):
        self.url = 'https://m.douban.com/rexxar/api/v2/movie/recommend?'  # 电影的列表
        self.surl = 'https://movie.douban.com/subject/'  # 电影详情页前
        self.headers = {  # 请求头
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63',
            'Referer': 'https://movie.douban.com/explore',
        }
        self.flag = 0  # 判断是否存在电影
        self.listTag = 0  # 初始化分类为2022年代
        self.ipList = []

    def init(self):  # 创建本地文件
        print('正在判断本地是否存在临时文件')
        if not os.path.exists('temp.csv'):  # 判断本地是否有csv
            print('临时文件不存在，正在创建')
            with open('temp.csv', 'w', newline='') as writer_f:
                writer = csv.writer(writer_f)
                writer.writerow(
                    ['directors', 'rate', 'title', 'casts', 'cover', 'detailLink', 'year', 'types', 'country', 'lang',
                     'time', 'movieTime', 'comment_len', 'starts', 'summary', 'comments', 'imgList', 'movieUrl'])
            print('临时文件创建成功')
        else:
            print('临时文件文件存在')
        print('正在判断本地是否存在页数记录文件')
        if not os.path.exists('Page.txt'):  # 保存当前所爬取的页数
            print('页数记录文件不存在，正在创建')
            with open('Page.txt', 'w', encoding='utf8') as f:
                f.write('0\n')
            print('页数记录文件创建成功')
        else:
            print('页数记录文件文件存在')
        print('查询是否已创建数据表movie')
        try:  # 在数据库中创建对应的表格
            con = connect(host='localhost', user='root', password='root', database='dbm', port=3306, charset='utf8mb4')
            sqlcommand = '''
                        create table movie (
                            id int primary key auto_increment,
                            directors varchar(500),
                            rate varchar(255),
                            title varchar(1000),
                            casts varchar(1000),
                            cover varchar(1000),
                            detailLink varchar(1000),
                            year varchar(255),
                            types varchar(1000),
                            country varchar(255),
                            lang varchar(255),
                            time varchar(255),
                            movieTime varchar(255),
                            comment_len varchar(255),
                            starts varchar(255),
                            summary varchar(1000),
                            comments text,
                            imgList varchar(1000),
                            movieUrl varchar(1000)
                        )
            '''
            cursor = con.cursor()
            cursor.execute(sqlcommand)
            con.commit()
            print('数据表movie未创建，正在创建')
            print('数据表movie创建成功')
        except:  # 如果表格存在则跳过
            print('数据表movie已存在')
            pass

    def ip_api(self):  # 判断是否请求到IP
        err = "请重新提取"
        errr = "再次请求"
        url = 'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=0&count=20&selected_categories=%7B%7D&tags=2022&ck=fG24'
        proxyMeta = ''
        while True:
            api = 'http://tiqu.pyhttp.taolop.com/getip?count=100&neek=46061&type=1&yys=0&port=1&sb=&mr=2&sep=4'
            re = requests.get(api).text.split('\n')
            ree = str(re)
            if ree.find(err) == -1 and ree.find(errr) == -1:
                for i in re:
                    self.ipList.append(i)
                print('获取到IP')
                proxyMeta = self.ipList[random.randint(0, len(self.ipList) - 2)]
                proxies = {
                    "http": proxyMeta,
                    "https": proxyMeta
                }
                try:
                    RowJson = requests.get(url, headers=self.headers, proxies=proxies, timeout=5).json()
                    print('该IP可用')
                    sleep(2)

                except:
                    print("此{0}不可用，跳过此IP".format(proxyMeta.replace("\n", "")))
                    self.ip_api()
                return proxyMeta
                break
            else:
                print('该请求未返回IP,等待2秒之后重新获取')
                print(re)
                sleep(2)
                continue

    def getPage(self):
        with open('Page.txt', 'r') as r_f:
            return r_f.readlines()[-1].strip()  # 返回之前爬取的最后一页的页数

    def setPage(self, newPage):
        with open('Page.txt', 'a') as w_f:
            w_f.write(str(newPage) + '\n')

    def spiderMain(self):
        page = self.getPage()
        param = {
            'refresh': 0,
            'start': int(page) * 20,
            'count': 20,
            'tags': List[self.listTag],
            'ck': 'fG24'
        }
        print('开始爬取{0}的电影,正在爬取第{1}页'.format(urllib.parse.unquote(str(List[self.listTag])), int(page) + 1))
        proxyMeta = self.ip_api()
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        try:
            RowJson = requests.get(self.url, headers=self.headers, params=param, proxies=proxies, timeout=5,
                                   verify=False).json()
        except:
            RowJson = {'items': []}
            print('该页没有内容')
            # pass
        # print(RowJson)# 请求电影页面数据
        itemJson = RowJson['items']  # 获取电影信息的item
        # print(itemJson)
        resultList = []
        try:
            for index, movieData in enumerate(itemJson):  # 爬取数据的主要代码
                if itemJson == []:
                    print('当前页面已经无数据，flag+1，flag为3的时候将爬取下一类,当前flag为{0}'.format(str(self.flag)))
                    self.flag = self.flag + 1
                    break
                print('正在爬取第%d条' % (index + 1))
                resultData = []
                id = itemJson[index]['id']
                print('电影id为{0}'.format(int(id)))
                finalurl = self.surl + id  # 用电影ID拼接URL出电影详情页URL
                finalJson = requests.get(finalurl, headers=self.headers, proxies=proxies, timeout=5,
                                         verify=False).text  # 请求详细页
                finalJsonXpath = etree.HTML(finalJson)
                # 电影导演（dicrectors）
                dicrectors = finalJsonXpath.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
                resultData.append(','.join(dicrectors))
                # 电影评分（rate)
                rate = finalJsonXpath.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')
                resultData.append(','.join(rate))
                # 电影名字（title)
                title = finalJsonXpath.xpath('//*[@id="content"]/h1/span[1]/text()')
                resultData.append(','.join(title))
                # 电影演员（casts)
                casts = []
                for i in finalJsonXpath.xpath('//*[@id="info"]//span[@class="actor"]//span[@class="attrs"]/a'):
                    casts.append(i.text)
                resultData.append(','.join(casts))
                # 电影封面（cover）
                cover = finalJsonXpath.xpath('//*[@id="mainpic"]/a/img/@src')
                resultData.append(','.join(cover))
                resultData.append(finalurl)
                # 电影年份（year）
                year = re.search('\d+', finalJsonXpath.xpath('//*[@id="content"]/h1/span[2]/text()')[0]).group()
                resultData.append(year)
                # 电影类型（types)
                types = []
                type = finalJsonXpath.xpath('//div[@id="info"]/span[@property="v:genre"]')
                for i in type:
                    types.append(i.text)
                resultData.append(','.join(types))
                # 电影制片国家（country）
                info = finalJsonXpath.xpath('//div[@id="info"]/text()')
                infos = []
                for i in info:
                    if i.strip() and not i.strip() == '/':
                        infos.append(i)
                resultData.append(','.join(infos[0].split(sep='/')).strip())
                # 语言（lang)
                try:
                    resultData.append(','.join(infos[1].split(sep='/')))
                except:
                    resultData.append('')
                # 上映时间（time)
                try:
                    time = finalJsonXpath.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[0][
                           :10]
                    resultData.append(time)
                except:
                    resultData.append(0)
                # 电影片长（movieTime)
                try:
                    movieTime = finalJsonXpath.xpath('//div[@id="info"]/span[@property="v:runtime"]/@content')
                    resultData.append(movieTime[0])
                except:
                    try:
                        resultData.append(re.search('\d+', infos[4]).group())
                    except:
                        resultData.append(random.randint(31, 69))
                # 短评个数（comment_len）
                resultData.append(re.search('\d+', finalJsonXpath.xpath(
                    '//div[@id="comments-section"]/div[@class="mod-hd"][1]/h2//a/text()')[0]).group())
                # 电影星级占比（starts）
                starts = []
                for i in finalJsonXpath.xpath(
                        '//div[@id="interest_sectl"]//div[@class="ratings-on-weight"]/div[@class="item"]'):
                    starts.append(i.xpath('./span[@class="rating_per"]/text()')[0])
                resultData.append(','.join(starts))
                # 电影简介（summary）
                resultData.append(finalJsonXpath.xpath('//span[@property="v:summary"]/text()')[0].strip())
                # 电影短评（comments）
                comments = []
                commentsList = finalJsonXpath.xpath('//div[@id="hot-comments"]/div')
                for i in commentsList:
                    x = 3
                    username = i.xpath('.//h3/span[@class="comment-info"]/a/text()')[0]
                    start = re.search('\d+', i.xpath('.//h3/span[@class="comment-info"]/span[2]/@class')[0])
                    if start == None:  # 判断短评是否有星级
                        x = 2
                        start = '0'
                    else:
                        start = re.search('\d+', i.xpath('.//h3/span[@class="comment-info"]/span[2]/@class')[0]).group()
                    times = i.xpath(f'.//h3/span[@class="comment-info"]/span[{x}]/@title')[0]
                    content = i.xpath('.//p[@class=" comment-content"]/span/text()')[0]
                    comments.append({
                        'user': username,
                        'start': start,
                        'time': times,
                        'content': content
                    })
                resultData.append(json.dumps(comments))

                # 图片列表（imgList）
                resultData.append(','.join(finalJsonXpath.xpath('//ul[contains(@class,"related-pic-bd ")]//img/@src')))
                # 电影预告片链接
                try:
                    movieUrl = \
                        finalJsonXpath.xpath(
                            '//ul[contains(@class,"related-pic-bd ")]/li[@class="label-trailer"]/a/@href')[0]
                    movieHtml = requests.get(movieUrl, headers=self.headers, proxies=proxies, timeout=5,
                                             verify=False)  # 请求预告片链接
                    movieHtmlXpath = etree.HTML(movieHtml.text)
                    resultData.append(movieHtmlXpath.xpath('//video/source/@src')[0])
                except:
                    resultData.append(0)

                resultList.append(resultData)
                print('此页爬取成功，重置flag')
                self.flag = 0


        except:
            print('无法获取当前页内容，flag+1，flag到3时则开始爬取下一类,当前flag为{0}'.format(str(self.flag)))
            self.flag = self.flag + 1

            pass

        self.saveToCsv(resultList)
        self.setPage(int(page) + 1)
        self.ipList = []
        self.ip_api()
        self.clearCsv()
        if self.flag > 3:
            print('{0}爬取完毕'.format(urllib.parse.unquote(str(List[self.listTag]))))
            self.listTag = self.listTag + 1
            self.flag = 0
            self.spiderMain()
            proxyMeta = ''
        elif self.listTag > 9:
            print('{0}爬取完毕'.format(urllib.parse.unquote(str(List[self.listTag]))))
        else:
            self.spiderMain()
            proxyMeta = ''

    def saveToCsv(self, resultList):
        print('正在保存信息到CSV')
        with open('temp.csv', 'a', newline='', encoding='utf-8') as f:
            saveData = csv.writer(f)
            for rowData in resultList:
                saveData.writerow(rowData)

    def clearCsv(self):
        print('正在清洗数据')
        df = pd.read_csv('temp.csv')
        df.dropna(inplace=True)  # 删除缺失值
        df.drop_duplicates()  # 删除重复值

    def saveSql(self):
        print('正在保存信息至SQL数据库')
        df = pd.read_csv('temp.csv', encoding='utf-8')
        df.to_sql('movie', con=engine, index=False, if_exists='append')
        print('保存成功')


if __name__ == '__main__':
    SpiderObj = spider()
    SpiderObj.init()
    sleep(3)
    # SpiderObj.spiderMain()
    SpiderObj.saveSql()
