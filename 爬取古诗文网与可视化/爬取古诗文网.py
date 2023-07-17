import csv, random, time
from selenium import webdriver
from selenium.webdriver.common.by import By

poetries = []
url = 'https://www.gushiwen.cn/'
web = webdriver.Chrome()


def get_data():
    title = web.find_elements(By.XPATH, '//*[@id="sonsyuanwen"]/div[1]/h1')[0].text
    author = web.find_elements(By.XPATH, '//*[@id="sonsyuanwen"]/div[1]/p/a[1]')[0].text
    dynasty = web.find_elements(By.XPATH, '//*[@id="sonsyuanwen"]/div[1]/p/a[2]')[0].text
    content = web.find_elements(By.XPATH, '//div[@class="contson"]')[0].text
    poetry = {"诗名": title, "作者": author, "朝代": dynasty, "古诗内容": content}
    poetries.append(poetry)
    return poetries


def save_data():
    with open('poetry_data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['诗名', '作者', '朝代', '古诗内容'])
        writer.writeheader()
        writer.writerows(poetries)


def main():
    web.get(url)
    time.sleep(2)
    a_hrefs = web.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/p[1]/a')
    for i, href in enumerate(a_hrefs):
        print("正在爬取第{}个".format(i + 1))
        web.execute_script('arguments[0].scrollIntoView();', href)  # 滑动到元素至可见
        href.click()
        web.switch_to.window(web.window_handles[1])
        time.sleep(random.randint(0, 2))
        get_data()
        web.close()
        web.switch_to.window(web.window_handles[0])
    print("数据爬取完毕！")
    save_data()


main()
web.close()
