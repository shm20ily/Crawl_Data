import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 中文和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

df1 = pd.read_csv('01.csv')
df2 = pd.read_csv('02.csv')
df = pd.concat([df1, df2], axis=1)  # 合并两个文件
df['招聘职位'] = df['招聘职位'].str.strip('个').astype(int).values  # 去掉中文字符，转化数字类型：字符串转为整数
df['面试评价'] = df['面试评价'].str.strip('个').astype(int).values  # 去掉中文字符，转化数字类型：字符串转为整数
df = df.reindex(columns=['全称', '简称', '行业领域', '公司规模', '招聘职位', '面试及时处理率', '面试评价'])  # 将公司名称放在前面
# df.to_csv('公司信息.csv', index=False)  # 保存合并后的文件，注意：第一次保存后注释掉该行代码再运行

fields = df['行业领域'].tolist()  # 清洗-->行业领域中的字符(保留中文字符)
field_li = []  # 将清洗后的中文字符添加到列表中，以便可视化
for f in fields:
    filed = f.split('｜')
    for i in filed:
        if ',' in i:
            t = i.split(',')
            for j in t:
                field_li.append(j)
        else:
            field_li.append(i)

s_f = pd.DataFrame({'行业领域': field_li}).value_counts()  # 统计行业领域的个数
s_value = s_f.values[:5]  # x轴
s_fields = s_f.index[:5].tolist()  # y轴
s_field = [str(i[0]) for i in s_fields]  # 提取列表里的元组元素
N = len(s_value)  # 设置雷达图的角度，用于平分切开一个圆面
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
# 绘图——————雷达图
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)  # 这里一定要设置为极坐标格式
ax.plot(angles, s_value, 'o-', linewidth=2)  # 绘制折线图
ax.fill(angles, s_value, alpha=0.25)  # 填充颜色
ax.set_thetagrids(angles * 180 / np.pi, s_field)  # 添加每个特征的标签
ax.set_ylim(0, 45)  # 设置雷达图的范围
plt.title('行业领域前五')  # 添加标题
ax.grid(True)  # 添加网格线

s_cpy = pd.DataFrame({'公司简称': df['简称'], '招聘职位数量': df['招聘职位']}).sort_values(by=['招聘职位数量'], ascending=False)[:6]
post_count = np.array(s_cpy['招聘职位数量'].values)
name = s_cpy['公司简称'].values
# 绘图——————条形图
plt.figure(figsize=(10, 6))
plt.bar(range(6), post_count, align='center', color='steelblue', alpha=0.8)
plt.xticks(range(6), name, rotation=45)  # 添加刻度标签
plt.xlabel('公司简称')
plt.ylabel('招聘职位数量')  # 添加y轴标签
plt.title('招聘职位数量前五')  # 添加标题
plt.ylim([0, 180])  # 设置y轴的刻度范围
for x, y in enumerate(post_count):  # 为每个条形图添加数值标签
    plt.text(x, y, '%s' % round(y, 1), ha='center')
plt.tight_layout()

s_eva = pd.DataFrame({'公司简称': df['简称'], '面试评价数': df['面试评价']}).sort_values(by=['面试评价数'], ascending=False)[:6]
eva_count = s_eva['面试评价数'].values
eva_name = s_eva['公司简称'].values
# 绘图——————折线图
plt.figure(figsize=(10, 6))
plt.plot(range(len(eva_count)),  # x轴数据
         eva_count,  # y轴数据
         linestyle='-',  # 折线类型
         linewidth=2,  # 折线宽度
         color='steelblue',  # 折线颜色
         marker='o',  # 点的形状
         markersize=6,  # 点的大小
         markeredgecolor='black',  # 点的边框色
         markerfacecolor='brown')  # 点的填充色
plt.title('面试评价数前五')  # 添加标题和坐标轴标签
plt.xlabel('公司简称')
plt.xticks(range(6), eva_name, rotation=45)  # 添加刻度标签
plt.ylabel('面试评价数')
plt.tight_layout()
plt.show()
