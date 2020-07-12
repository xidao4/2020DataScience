from sklearn.cluster import KMeans
from sklearn import metrics
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def handle_data():
    data = pd.read_csv('pro_with_features.csv')
    # 特征选择
    features = ['1a_rate', 'ac_rate', 'total_submit']
    features_data = data[features]
    # print(features_data)
    a1_rate_s = features_data['1a_rate']
    # print(a1_rate_s)
    a1_rate_s = (a1_rate_s - a1_rate_s.min()) / (a1_rate_s.max() - a1_rate_s.min())
    # print(a1_rate_s)
    ac_rate_s = features_data['ac_rate']
    ac_rate_s = (ac_rate_s - ac_rate_s.min()) / (ac_rate_s.max() - ac_rate_s.min())
    total_submit_s = features_data['total_submit']
    total_submit_s = (total_submit_s - total_submit_s.min()) / (total_submit_s.max() - total_submit_s.min())
    features_data.loc[:,'1a_rate'] = a1_rate_s
    #print(ac_rate_s)
    features_data.loc[:,'ac_rate'] = ac_rate_s
    features_data.loc[:,'total_submit'] = total_submit_s
    print(features_data)
    return features_data

if __name__=='__main__':
    features_data=handle_data()
    #param()
    # for i in range(3,6):
    #     print(i)
    #     y_pred=KMeans(n_clusters=i,random_state=9).fit_predict(features_data)
    #     print(metrics.calinski_harabasz_score(features_data,y_pred))
    fig=plt.figure()
    ax=Axes3D(fig)
    x=features_data.loc[:,'1a_rate']
    y=features_data.loc[:,'ac_rate']
    z=features_data.loc[:,'total_submit']
    #print(z)
    ax.scatter(x,y,z)
    ax.set_zlabel('total_submit')
    ax.set_ylabel('ac_rate')
    ax.set_xlabel('1a_rate')
    plt.savefig('fig.png',bbox_inches='tight')

