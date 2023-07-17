import jieba
import jieba.analyse
import re
import pandas as pd
from pyecharts.charts import WordCloud

punc = '~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}【】'
data1 = pd.read_csv('去哪儿.csv')


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
