import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
'''
读取pro_with_features_difficulty.csv（根据每道题的分值将题目分为ABC三种难度等级）
进行双变量相关性分析：spearman相关评估两个连续变量之间的单调关系
'''
def draw():
    csvfile=open('pro_with_features_difficulty.csv','r')
    lines=csvfile.readlines()
    csvfile.close()
    rows=[]
    for line in lines:
        rows.append(line.split(','))
    scores=[]
    total_submits=[]
    score_rates=[]
    for i in rows:
        scores.append(i[1])
        total_submits.append(i[7])
        score_rates.append(i[6])
    scores=scores[1:]
    total_submits=total_submits[1:]
    score_rates=score_rates[1:]
    scores=list(map(int,scores))
    total_submits=list(map(float,total_submits))
    score_rates=list(map(float,score_rates))

#画散点图
    #中文显示默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    area = np.pi * 4 ** 2#散点大小
    colors1 = '#00CED1'#颜色设置
    colors2 = '#DC143C'


    plt.scatter(scores,total_submits,s=area,c=colors1)
    plt.xlabel("score")
    plt.ylabel("total_submits")
    plt.show()

    plt.yticks(np.linspace(0, 100, 11), size=18) #设置y轴刻度
    plt.xticks(np.linspace(0, 2500, 11), size=18)#设置x轴刻度
    plt.scatter(scores, score_rates, s=area,c=colors2)
    plt.xlabel("score")
    plt.ylabel("score_rate")
    plt.show()
    return True

if __name__=='__main__':
    data = pd.read_csv('pro_with_features_difficulty.csv')
    print(data)

    print('ac_rate')
    print(data['score'].corr(data['ac_rate'], method='spearman'))#-0.266

    print('1a_rate')
    print(data['score'].corr(data['1a_rate'], method='spearman'))#-0.122

    print('total_submit')
    print(data['score'].corr(data['total_submit'], method='spearman'))#-0.906

    print('avg_ac_time')
    print(data['score'].corr(data['avg_ac_time'], method='spearman'))#-0.184
    #print(data['difficulty_level'].corr(data['avg_ac_time'], method='spearman'))#-0.218

    print('score_rate')
    print(data['score'].corr(data['score_rate'], method='spearman'))#-0.461

    print('user_Nums')
    print(data['score'].corr(data['user_Nums'], method='spearman'))#-0.920

    draw()#画散点图

