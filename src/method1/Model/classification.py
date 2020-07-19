#encoding=utf-8
import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.model_selection import cross_validate

'''
adoboost分类器：
    调优参数
        param()方法：对AdoBoost框架学习器个数进行择优
        param2()方法：对AdoBoost所集成的弱分类树的深度进行择优
    准确评估
'''

def param(train_features, test_features, train_labels, test_labels):
    # 对框架参数，如学习器个数进行择优
    param_test1 = {"n_estimators": range(116, 132, 2)}
    estimatorCart = DecisionTreeClassifier()
    gsearch1 = GridSearchCV(estimator=AdaBoostClassifier(estimatorCart),
                            param_grid=param_test1) #, scoring="roc_auc", cv=5
    gsearch1.fit(train_features, train_labels)
    print(gsearch1.best_params_, gsearch1.best_score_)

def param2(train_features, test_features, train_labels, test_labels):
    tree_depth=0
    samples_split=0
    score=0
    for i in range(1, 3):  # 决策树最大深度循环
        print(i)
        for j in range(18, 23):
            print(j)
            bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=i,min_samples_split=j), n_estimators=124)
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

def adoboost(train_features,test_features,train_labels,test_labels):
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1,min_samples_split=19), n_estimators=124)
    clf.fit(train_features, train_labels)
    pred_labels = clf.predict(test_features)
    score = accuracy_score(test_labels, pred_labels)
    print("adaboost分类树准确率 %.4lf" % score)
    return test_labels, pred_labels

def get_features_data_labels_data():
    # 数据加载
    f = open("../PDI/d_difficulty_dict_with_metrics_2.json", encoding="utf8")
    res = f.read()
    diff_dict = json.loads(res)
    data = []
    for v in diff_dict.values():
        inner_lst = []
        inner_lst.append(int(v["case_id"]))
        #修改：下两行的avg_cc_score与avg_cc_level互换
        inner_lst.append(v["avg_cc_score"])
        inner_lst.append(v["avg_cc_level"])
        inner_lst.append(v["avg_LLOC"])
        inner_lst.append(v["avg_unique_operator_Nums"])
        inner_lst.append(v["avg_unique_operand_Nums"])
        inner_lst.append(v["avg_operator_Nums"])
        inner_lst.append(v["avg_operand_Nums"])
        inner_lst.append(v["RDI"])
        data.append(inner_lst)
    print('读出的json数据')
    print(data)
    col_name = ["case_id", "avg_cc_level", "avg_cc_score", "avg_LLOC", "avg_unique_operator_Nums",
                "avg_unique_operand_Nums", "avg_operator_Nums", "avg_operand_Nums", "RDI"]
    data = pd.DataFrame(data, columns=col_name)
    print('转换为dataframe的数据')
    print(data)
    # 去除空行
    data.dropna(how='any', inplace=True)
    #根据散点图，可知D等级题目的各项software metrics不规律，故去除RDI为D的行
    data.drop(data[data.RDI=='D'].index,inplace=True)
    print('去除RDI为D的行后的dataframe')
    print(data)
    # 数据探索
    # print(data.describe())

    # 特征选择
    features = ["avg_cc_score", "avg_LLOC",  "avg_unique_operand_Nums"]
    features_data = data[features]
    # # # # #
    # features_data.loc[:, 'halstead'] = features_data.apply(total_halstead, axis=1)
    print('最终选择得特征数据')
    print(features_data)
    labels_data = data["RDI"]
    print('最终的结果')
    print(labels_data)
    return features_data,labels_data

def get_train_test_split():
    features_data,labels_data=get_features_data_labels_data()
    # 划分训练集 测试集
    train_features, test_features, train_labels, test_labels = train_test_split(features_data, labels_data,
                                                                                test_size=0.25,random_state=4)
    print('训练集的特征数据')
    print(train_features)
    print('训练集的结果')
    print(train_labels)
    print('测试集的特征数据')
    print(test_features)
    print('测试集的结果')
    print(test_labels)
    return train_features,test_features,train_labels,test_labels

if __name__=='__main__':

    train_features,test_features,train_labels,test_labels=get_train_test_split()


    '''
    调优参数
    '''
    # 对AdoBoost框架学习器个数进行择优↓
    # param(train_features,test_features,train_labels,test_labels)

    # 对AdoBoost所集成的弱分类树的深度进行择优↓
    # param2(train_features,test_features,train_labels,test_labels)


    '''
    调用参数调优过的adoboost()，评估准确率
    '''
    adoboost(train_features,test_features,train_labels,test_labels)







