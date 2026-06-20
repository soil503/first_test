# conding: utf-8
import sys
 
import pandas as pd
 
data = pd.read_csv(sys.argv[1], sep="\t", header=None)
 
new = data[1].str.split('.').str
data['id'] = new[0].values
data['cha'] = data[3] - data[2]
 
for name, group in data.groupby(['id']):
    if len(group) == 1:
        continue
    ind = group.sort_values(by='cha', ascending=False).index[1:].values
    data.drop(index=ind, inplace=True)
 
# data[2] =data[2].astype(int)
# data[3] =data[3].astype(int)
# for name, group in data.groupby(0):
#     if len(group) == 1:
#         continue
#     start=0
#     # print(group.head())
#     group = group.sort_values(by=[2,3],ascending=[True,False])
#     for index, row in group.iterrows():
#         # print(row)
#         if row[3]>start or row[2]>start:
#             start=max([row[3],row[2]])
#             continue
#         data.drop(index=index, inplace=True)
# ind = group.sort_values(by='cha', ascending=False).index[1:].values
# print(name)
# print(group.sort_values(by='cha',ascending=False))
 
 
# data = data[data[1].str.contains('\.mRNA1$')]
data['order'] = ''
data['newname'] = ''
print(data.head())
for name, group in data.groupby([0]):
    number = len(group)
    # 统计每条染色体最后一个基因的最后一个核苷酸的位置  不一定准确
    group = group.sort_values(by=[2])
    data.loc[group.index, 'order'] = list(range(1, len(group) + 1))
    data.loc[group.index, 'newname'] = list(
        ['gl' + str(name) + 'g' + str(i).zfill(5) for i in range(1, len(group) + 1)])
data['order'] = data['order'].astype('int')
data = data[[0, 'newname', 2, 3, 4, 'order', 1]]
print(data.head())
# 原来没有下面这行，那就是对data第1列的字符串"1""2""3".."10"进行排列，这会导致10 排在2的前面
data[0] = pd.to_numeric(data[0], errors='coerce')
data = data.dropna(subset=[0])
data[0] = data[0].astype(int)
data = data.sort_values(by=[0, 'order'])
# 再将data第一列的值转回str类型
data[0] = data[0].astype(str)
data.to_csv(sys.argv[2], sep="\t", index=False, header=None)
lens = data.groupby(0).max()[[3, 'order']]
lens.to_csv(sys.argv[3], sep="\t", header=None)
 
print("新gff和lens生成成功")
