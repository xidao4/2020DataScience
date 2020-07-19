
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier

'''
采用AdaBoost机器算法进行分类：
    调优参数
        param()方法：对AdoBoost框架学习器个数进行择优
        param2()方法：对AdoBoost所集成的弱分类树的深度进行择优
    总体和分题型的平均准确率评估
'''

def AdaBoost():
    data = pd.read_csv('pro_with_features_difficulty.csv')
    # 特征选择
    features = ['1a_rate', 'ac_rate', 'total_submit','avg_ac_time','score_rate']
    features_data = data[features]
    labels_data = data['difficulty_level']
    # 划分训练集 测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features_data, labels_data,
                                                                                test_size=0.25)  # random_state
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=2,min_samples_split=19), n_estimators=137)
    clf.fit(train_features, train_labels)
    pred_labels = clf.predict(test_features)
    score = accuracy_score(test_labels, pred_labels)
    print("adaboost分类树准确率 %.4lf" % score)
    return test_labels, pred_labels,score

from sklearn.model_selection import GridSearchCV

def param():
    data = pd.read_csv('pro_with_features_difficulty.csv')
    # 特征选择
    features = ['1a_rate', 'ac_rate', 'total_submit','avg_ac_time','score_rate']
    features_data = data[features]
    labels_data = data['difficulty_level']
    # 划分训练集 测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features_data, labels_data,test_size=0.25)  # random_state
    # 对框架参数，如学习器个数进行择优
    param_test1 = {"n_estimators": range(131, 138, 1)}
    estimatorCart = DecisionTreeClassifier()
    gsearch1 = GridSearchCV(estimator=AdaBoostClassifier(estimatorCart),
                            param_grid=param_test1) #, scoring="roc_auc", cv=5
    gsearch1.fit(train_features, train_labels)
    print(gsearch1.best_params_, gsearch1.best_score_)

import numpy as np
from sklearn.model_selection import cross_validate

def param2():
    data = pd.read_csv('pro_with_features_difficulty.csv')
    # 特征选择
    features = ['1a_rate', 'ac_rate', 'total_submit','avg_ac_time','score_rate']
    features_data = data[features]
    labels_data = data['difficulty_level']
    # 划分训练集 测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features_data,
                                                                                labels_data,test_size=0.25)  # random_state
    tree_depth=0
    samples_split=0
    score=0
    for i in range(1, 3):  # 决策树最大深度循环
        print(i)
        for j in range(18, 22):
            print(j)
            bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=i,min_samples_split=j), n_estimators=137)
            cv_result = cross_validate(bdt, train_features, train_labels, return_train_score=False, cv=5)
            cv_value_vec = cv_result["test_score"]
            cv_mean = np.mean(cv_value_vec)
            if cv_mean >= score:
                score = cv_mean
                tree_depth = i
                samples_split = j
    print(tree_depth)
    print(samples_split)
    return tree_depth,samples_split

def assessment(test_labels,pred_labels):
    a1=0
    a2=0
    b1=0
    b2=0
    c1=0
    c2=0
    for i in range(len(test_labels)):
        if test_labels[i]=='A':
            a1+=1
            if pred_labels[i]=='A':
                a2+=1
        elif test_labels[i]=='B':
            b1+=1
            if pred_labels[i]=='B':
                b2+=1
        elif test_labels[i]=='C':
            c1+=1
            if pred_labels[i]=='C':
                c2+=1
    a_rate=a2/a1*100
    b_rate=b2/b1*100
    c_rate=c2/c1*100
    print('A类型题目，共',a1,'题,预测正确有',a2,'题,预测准确率为',a_rate)
    print('B类型题目，共', b1, '题,预测正确有', b2, '题,预测准确率为', b_rate)
    print('C类型题目，共', c1, '题,预测正确有', c2, '题,预测准确率为', c_rate)
    return a_rate,b_rate,c_rate

if __name__=='__main__':
    '''
    调优参数
    '''
    #对AdoBoost框架学习器个数进行择优↓
    #param()

    #对AdoBoost所集成的弱分类树的深度进行择优↓
    #param2()


    '''
    调用参数调优过的adoboost()，评估准确率
    '''
    a=0
    b=0
    c=0
    total_score=0
    for i in range(10):
        print(i)
        test_labels,pred_labels,score=AdaBoost()
        a_rate,b_rate,c_rate=assessment(list(test_labels.values),pred_labels)
        total_score+=score
        a+=a_rate
        b+=b_rate
        c+=c_rate
    print()
    print('平均准确率为',total_score/10)
    print('A类型题目预测准确率为',a/10)
    print('B类型题目预测准确率为',b/10)
    print('C类型题目预测准确率为', c/10)




