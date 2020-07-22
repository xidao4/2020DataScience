import json
import os
import shutil
import sys
from six.moves import urllib
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# TO可视化

# 目前用的数据还是s_record_dict.json
f = open("s_record_dict.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

# 目前用的数据还是s_pro_detail_dict.json
f = open("s_pro_detail_dict.json", encoding="utf8")
res = f.read()
data2 = json.loads(res)
data2 = list(dict.values(data2))

numofProString = 0  # 字符串代码数量
numofProList = 0    # 数组代码数量
numofProPhoto = 0   # 图代码数量
numofProTree = 0    # 树代码数量
numofProLinear = 0  # 线性表代码数量
numofProSearch = 0  # 查找算法代码数量
numofProNumope = 0  # 数字操作代码数量
numofProSort = 0    # 排序算法代码数量

numofTO_String = 0  # 字符串题目TO代码数量
numofTO_List = 0    # 数组题目TO代码数量
numofTO_Photo = 0   # 图题目TO代码数量
numofTO_Tree = 0    # 树题目TO代码数量
numofTO_Linear = 0  # 线性表题目TO代码数量
numofTO_Search = 0  # 查找算法TO代码数量
numofTO_Numope = 0  # 数字操作TO代码数量
numofTO_Sort = 0    # 排序算法TO代码数量

caseidOfTO = []  # 存面向用例代码对应的case_id  可重复
allCaseId = []  # 存所有代码对应的case_id  可重复

temp = []
for item in data2:
    temp.append(item["case_type"])
temp = list(set(temp))


def getproTypebycaseId(caseid):  # 通过caseid获取casetype
    for item in data2:
        if item["case_id"] == caseid:
            return item["case_type"]


for item in data:
    if item["is_TO"]:
        caseidOfTO.append(item["case_id"])

    allCaseId.append(item["case_id"])

for item in data2:  # 拿到各自题目类型的代码提交总数
    if item["case_type"] == "字符串":
        numofProString += allCaseId.count(item["case_id"])
    elif item["case_type"] == "数组":
        numofProList += allCaseId.count(item["case_id"])
    elif item["case_type"] == "图结构":
        numofProPhoto += allCaseId.count(item["case_id"])
    elif item["case_type"] == "树结构":
        numofProTree += allCaseId.count(item["case_id"])
    elif item["case_type"] == "排序算法":
        numofProSort += allCaseId.count(item["case_id"])
    elif item["case_type"] == "查找算法":
        numofProSearch += allCaseId.count(item["case_id"])
    elif item["case_type"] == "线性表":
        numofProLinear += allCaseId.count(item["case_id"])
    elif item["case_type"] == "数字操作":
        numofProNumope += allCaseId.count(item["case_id"])

for caseid in caseidOfTO:  # 拿到各自题目类型的TO代码提交总数
    if getproTypebycaseId(caseid) == "字符串":
        numofTO_String += 1
    if getproTypebycaseId(caseid) == "数组":
        numofTO_List += 1
    if getproTypebycaseId(caseid) == "图结构":
        numofTO_Photo += 1
    if getproTypebycaseId(caseid) == "树结构":
        numofTO_Tree += 1
    if getproTypebycaseId(caseid) == "排序算法":
        numofTO_Sort += 1
    if getproTypebycaseId(caseid) == "查找算法":
        numofTO_Search += 1
    if getproTypebycaseId(caseid) == "线性表":
        numofTO_Linear += 1
    if getproTypebycaseId(caseid) == "数字操作":
        numofTO_Numope += 1

num_list = []
num_list.append(float(format(numofTO_List / numofProList, '.3f')))
num_list.append(float(format(numofTO_Sort / numofProSort, '.3f')))
num_list.append(float(format(numofTO_Tree / numofProTree, '.3f')))
num_list.append(float(format(numofTO_Photo / numofProPhoto, '.3f')))
num_list.append(float(format(numofTO_Search / numofProSearch, '.3f')))
num_list.append(float(format(numofTO_Numope / numofProNumope, '.3f')))
num_list.append(float(format(numofTO_Linear / numofProLinear, '.3f')))
num_list.append(float(format(numofTO_String / numofProString, '.3f')))
# 画条形图
# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
label_list = ["数组", "排序算法", "树结构", "图结构", "查找算法", "数字操作", "线性表", "字符串"]  # 横坐标
# num_list1 = [0.914, 0.961, 0.959, 0.967, 0.968, 0.970,0.5,0.6]      # 横坐标值1,Baseline
num_list1 = num_list

# num_list2 = [0.902, 0.961, 0.959, 0.960, 0.966, 0.971]       # 横坐标值2,chi2
x = range(len(num_list1))
width = 0.24
mid_width = 0.04
plt.grid(axis="y", c='gray', linestyle='-')
rects1 = plt.bar(x, num_list1, width=width, color='#5F95D3', label="TO率", zorder=4)  # 设置zorder可以让柱状图不被网格线挡在前面，数字越大优先级越高
# rects2 = plt.bar([i + (width+mid_width) for i in x], num_list2, width=width, color='#BC524A', label="F1", zorder=4)
plt.ylim(0.0, 0.5)  # y轴取值范围
size = 18
plt.ylabel('TO率', size=size)
plt.xlabel('题目类型', size=size)
plt.xticks([i + (width + mid_width) / 2 for i in x], label_list, size=size)
plt.yticks(np.linspace(0, 0.5, 6), ['0%', '10%', '20%', '30%', '40%', '50%'], size=size)
plt.title("各题目类型TO率", size=size)
plt.legend(prop={'size': size}, bbox_to_anchor=(1, 1))  # 设置题注, bbox_to_anchor控制图例位置
# plt.savefig('base_chi2.png')
plt.show()
