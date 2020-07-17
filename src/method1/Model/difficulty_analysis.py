#encoding=utf-8
import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import calinski_harabasz_score
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.model_selection import cross_validate

def total_halstead(arrLike):
    return arrLike['avg_unique_operand_Nums']

def cart(train_features,test_features,train_labels,test_labels):
    # print(6)
    # print(train_labels)
    # print()

    # dvec=DictVectorizer(sparse=False)
    # #得到转化后的训练集的特征值矩阵
    # train_features=dvec.fit_transform(train_features.to_dict('record'))
    # print('转换后的特征属性',dvec.feature_names_)
    clf = DecisionTreeClassifier()
    clf.fit(train_features, train_labels)
    # #决策树可视化  必须在fit后执行，在predict之后运行会报错
    # import graphviz
    # from sklearn import tree
    # dot_data=tree.export_graphviz(clf,feature_names=dvec.feature_names_,filled=True)
    # graph=graphviz.Source(dot_data)
    # graph.render("tree")

    # 得到转换后的测试集的特征值矩阵
    # test_features=dvec.transform(test_features.to_dict(orient='record'))
    pred_labels = clf.predict(test_features)
    score = accuracy_score(test_labels, pred_labels)
    print("CART分类树准确率 %.4lf" % score)

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
    #param(train_features,test_features,train_labels,test_labels)
    #tree_depth,sample_split=param2(train_features,test_features,train_labels,test_labels)
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1,min_samples_split=19), n_estimators=124)
    clf.fit(train_features, train_labels)
    pred_labels = clf.predict(test_features)
    score = accuracy_score(test_labels, pred_labels)
    print("adaboost分类树准确率 %.4lf" % score)
    return test_labels, pred_labels

def kmeans(features_data):
    # 标准化
    features_data = preprocessing.scale(features_data)
    features_data = pd.DataFrame(features_data, columns=['avg_cc_score', 'avg_LLOC', 'halstead'])
    print('标准化后的特征数据')
    print(features_data)
    my_draw(features_data)
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features_data)
    predict_y = kmeans.predict(features_data)
    print('KMeans', calinski_harabasz_score(features_data, predict_y))

def corr():
    f = open("../PDI/d_difficulty_dict_with_metrics_2.json", encoding="utf8")
    res = f.read()
    diff_dict = json.loads(res)
    data=[]
    for v in diff_dict.values():
        inner_lst = []
        if v['avg_cc_level'] != None:
            inner_lst.append(float(v["avg_cc_level"]))
        if v['avg_LLOC']!=None:
            inner_lst.append(float(v["avg_LLOC"]))
        if v['avg_unique_operator_Nums']!=None and v['avg_unique_operand_Nums']!=None and v['avg_operator_Nums']!=None and v['avg_operand_Nums']!=None:
            inner_lst.append(v["avg_unique_operator_Nums"])
            inner_lst.append(v["avg_unique_operand_Nums"])
            inner_lst.append(v["avg_operator_Nums"])
            inner_lst.append(v["avg_operand_Nums"])
            inner_lst.append(v["avg_unique_operand_Nums"]+v["avg_operator_Nums"]+v["avg_operand_Nums"])
        inner_lst.append(v["avg_score"])
        data.append(inner_lst)
    col_name = ["avg_cc_score", "avg_LLOC", "avg_unique_operator_Nums",
                "avg_unique_operand_Nums", "avg_operator_Nums", "avg_operand_Nums", 'total_halstead',"avg_score"]
    data = pd.DataFrame(data, columns=col_name)
    # 去除空行
    data.dropna(how='any', inplace=True)
    print(data['avg_score'].corr(data['avg_cc_score'], method='spearman'))#-0.179
    print(data['avg_LLOC'].corr(data['avg_score'], method='spearman'))#-0.27170759185896465
    print(data['avg_unique_operator_Nums'].corr(data['avg_score'], method='spearman'))#-0.22232317252845155
    print(data['avg_unique_operand_Nums'].corr(data['avg_score'], method='spearman'))#-0.294692331701343
    print(data['avg_operand_Nums'].corr(data['avg_score'], method='spearman'))#-0.2791121197146751
    print(data['avg_operator_Nums'].corr(data['avg_score'], method='spearman'))#-0.27715071755751014
    print(data['total_halstead'].corr(data['avg_score'], method='spearman')) #-0.28572732631947056

def get_features_data_labels_data():
    # 数据加载
    f = open("../PDI/d_difficulty_dict_with_metrics_2.json", encoding="utf8")
    res = f.read()
    diff_dict = json.loads(res)
    data = []
    for v in diff_dict.values():
        inner_lst = []
        inner_lst.append(int(v["case_id"]))
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
    #去除RDI为D的行
    data.drop(data[data.RDI=='D'].index,inplace=True)
    print('去除RDI为D的行后的dataframe')
    print(data)
    # 数据探索
    # print(2)
    # print(data.describe())
    # print()

    # 特征选择
    features = ["avg_cc_score", "avg_LLOC", "avg_unique_operator_Nums", "avg_unique_operand_Nums", "avg_operator_Nums",
                "avg_operand_Nums"]
    features_data = data[features]
    # # 写得有问题
    # features_data.loc[:, 'halstead'] = features_data.apply(total_halstead, axis=1)
    features_data = features_data.drop(["avg_unique_operator_Nums", "avg_operator_Nums", "avg_operand_Nums"], axis=1)
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

def my_draw(features_data):
    fig = plt.figure()
    ax = Axes3D(fig)
    x = features_data.loc[:, 'avg_cc_score']
    y = features_data.loc[:, 'avg_LLOC']
    z = features_data.loc[:, 'halstead']
    # print(z)
    ax.scatter(x, y, z)
    ax.set_zlabel('avg_cc_score')
    ax.set_ylabel('avg_LLOC')
    ax.set_xlabel('halstead')
    plt.savefig('fig.png', bbox_inches='tight')

if __name__=='__main__':
    train_features,test_features,train_labels,test_labels=get_train_test_split()
    #cart(train_features,test_features,train_labels,test_labels)
    adoboost(train_features,test_features,train_labels,test_labels)

    #features_data=get_features_data_labels_data()[0]
    #print('数据归一前')
    #print(features_data)
    #kmeans(features_data)

    #corr()





