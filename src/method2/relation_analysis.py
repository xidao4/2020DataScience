import pandas as pd

'''
读取pro_with_features_difficulty.csv（根据每道题的分值将题目分为ABC三种难度等级）
进行双变量相关性分析：spearman相关评估两个连续变量之间的单调关系
'''

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

