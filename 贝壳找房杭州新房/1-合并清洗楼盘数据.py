import pandas as pd

# df1 = pd.read_csv("loupan.csv")
# df2 = pd.read_csv("loupan1.csv")
# df3 = pd.read_csv("loupan2.csv")
# df4 = pd.read_csv("loupan3.csv")
# df = pd.concat([df1, df2, df3, df4])
# df = df.reset_index(drop=True)
# print(df)
# df.info()
# df.to_csv("loupanshuju.csv")

df5 = pd.read_csv("beike.csv")
df5 = df5.drop(columns=['楼盘链接'])
# print(df5)
# df5.info()

df7 = pd.read_csv("loupanshuju.csv")
df7 = df7.drop(columns=["Unnamed: 0"])
# print(df7)

df6 = pd.concat([df5, df7], axis=1)
print(df6)
df6.to_csv("楼盘数据.csv")
