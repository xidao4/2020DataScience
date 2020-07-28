import json
import os
import shutil
import sys
from six.moves import urllib
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
#学生TO可视化

f = open("d_record_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

student_id=[]

for item in data:
    student_id.append(item["user_id"])
student_id=list(set(student_id))      #拿到所有学生ID
num_of_stu=len(student_id)
all_record=[0]*len(student_id)
to_record=[0]*len(student_id)
for item in data:                     #遍历一遍拿到学生的所有代码和TO代码数量
    all_record[student_id.index(item["user_id"])]+=1
    if item["is_TO"]:
        to_record[student_id.index(item["user_id"])]+=1
record_T0=[]
for i,j in zip(to_record , all_record):    #TO比例
    record_T0.append(float(format(i/j,'.3f')))  #保留三位小数
record_T0.sort()

persentofTo=['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
totalNumofstu=[0]*10
for ix in range(1,11):
    for i in record_T0:
        if i<ix/10:
            totalNumofstu[ix-1]+=1

for i in range(0,len(totalNumofstu)):
    totalNumofstu[len(totalNumofstu)-i-1]-=totalNumofstu[len(totalNumofstu)-1-i-1]
#取到各个百分段直接的人数
percentofStuTO=[]
for i in totalNumofstu:
    percentofStuTO.append(i/len(student_id))
#取到百分比











#画图

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
#人数图
label_list = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']    # 横坐标刻度显示值
num_list1=totalNumofstu
x = range(len(num_list1))
width = 1
mid_width = 0.04
plt.grid(axis="y", c='gray', linestyle='-')
rects1 = plt.bar(x, num_list1, width=width, color='#5F95D3', label="多少人", zorder=4)  # 设置zorder可以让柱状图不被网格线挡在前面，数字越大优先级越高
plt.ylim(0.0, 100)     # y轴取值范围
size = 18
plt.ylabel('学生人数',size=size)
plt.xlabel('TO率',size=size)
plt.xticks([i + (width+mid_width)/2 for i in x], label_list, size=size)
plt.yticks(np.linspace(0, 100, 10),['10','20','30','40','50','60','70','80','90','100'], size=size)
plt.title("TO率的学生人数", size=size)
plt.legend(prop={'size': size}, bbox_to_anchor=(1, 1))     # 设置题注, bbox_to_anchor控制图例位置
# plt.savefig('base_chi2.png')
plt.show()


#人数比例图
width=1
plt.grid(axis="y", c='gray', linestyle='-')
rects2 = plt.bar(x, percentofStuTO, width=width, color='#5F95D3', label="人数比例", zorder=4)
plt.ylim(0.0, 1)     # y轴取值范围
plt.ylabel('人数比例',size=size)
plt.xlabel('TO率',size=size)
plt.xticks([i + (width+mid_width)/2 for i in x], label_list, size=size)
plt.yticks(np.linspace(0, 1, 11), [ '0%','10%', '20%', '30%', '40%', '50%','60%','70%','80%','90%','100%'], size=size)
plt.title("TO率的学生比例", size=size)
plt.legend(prop={'size': size}, bbox_to_anchor=(1, 1))     # 设置题注, bbox_to_anchor控制图例位置
plt.show()