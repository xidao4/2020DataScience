import pandas as pd

if __name__=='__main__':
    data = pd.read_csv('pro_with_features_difficulty.csv')
    print(data)
    print('ac_rate')
    print(data['score'].corr(data['ac_rate'], method='spearman'))#0.266
    print(data['difficulty_level'].corr(data['ac_rate'],method='spearman'))
    print('1a_rate')
    print(data['score'].corr(data['1a_rate'], method='spearman'))#0.122
    print(data['difficulty_level'].corr(data['1a_rate'], method='spearman'))
    print('total_submit')
    print(data['score'].corr(data['total_submit'], method='spearman'))#0.906
    print(data['difficulty_level'].corr(data['total_submit'], method='spearman'))
    print('avg_ac_time')
    print(data['score'].corr(data['avg_ac_time'], method='spearman'))#0.184
    print(data['difficulty_level'].corr(data['avg_ac_time'], method='spearman'))#0.218
    print('score_rate')
    print(data['score'].corr(data['score_rate'], method='spearman'))#0.461
    print(data['difficulty_level'].corr(data['score_rate'], method='spearman'))
    print('user_Nums')
    print(data['score'].corr(data['user_Nums'], method='spearman'))#0.920
    print(data['difficulty_level'].corr(data['user_Nums'], method='spearman'))