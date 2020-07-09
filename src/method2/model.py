
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import calinski_harabasz_score

def CART():
    data=pd.read_csv('pro_with_features.csv')
    print(data)
    print()
    print()
    #特征选择
    features=['1a_rate','avg_ac_time','score_rate','total_submit','ac_Nums']
    features_data=data[features]
    print('features_data')
    print(features_data)
    print()
    print()
    labels_data=data['difficulty_level']
    print('labels_data')
    print(labels_data)
    print()
    print()
    #划分训练集 测试集
    train_features,test_features,train_labels,test_labels=train_test_split(features_data,labels_data,test_size=0.25,random_state=0)
    print('train_features')
    print(train_features)
    print()
    print()
    print('train_labels')
    print(train_labels)
    print()
    print()
    print('test_features')
    print(test_features)
    print()
    print()
    print('test_labels')
    print(test_labels)
    print()
    print()
    clf=DecisionTreeClassifier()
    clf.fit(train_features,train_labels)
    pred_labels=clf.predict(test_features)
    print('pred_labels')
    print(pred_labels)
    print()
    print()
    score=accuracy_score(test_labels,pred_labels)
    print("CART分类树准确率 %.4lf" % score)

def AdaBoost():
    data = pd.read_csv('pro_with_features.csv')
    # 特征选择
    features = ['1a_rate', 'avg_ac_time', 'score_rate', 'total_submit', 'ac_Nums']
    features_data = data[features]
    labels_data = data['difficulty_level']
    # 划分训练集 测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features_data, labels_data,test_size=0.25,random_state=0)
    clf = AdaBoostClassifier()
    clf.fit(train_features, train_labels)
    pred_labels = clf.predict(test_features)
    score = accuracy_score(test_labels, pred_labels)
    print("adaboost分类树准确率 %.4lf" % score)

def my_kmeans():
    data = pd.read_csv('pro_with_features.csv')
    # 特征选择
    features = ['1a_rate', 'avg_ac_time', 'score_rate', 'total_submit', 'ac_Nums']
    train_features = data[features]
    #标准化到[-1,1]空间
    z_score_scaler=preprocessing.ZScoreScaler()
    train_features=z_score_scaler.fit_transform(train_features)
    #kmeans算法
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(train_features)
    predict_y=kmeans.predict(train_features)
    print('KMeans',calinski_harabasz_score(train_features,predict_y))

def EM():
    return


if __name__=='__main__':
    CART()
    AdaBoost()
    #my_kmeans()
    EM()