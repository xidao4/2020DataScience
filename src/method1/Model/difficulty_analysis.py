#encoding=utf-8
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#数据加载
f=open("../PDI/s_difficulty_dict_with_metrics.json",encoding="utf8")
res=f.read()
diff_dict=json.loads(res)
data=[]
for v in diff_dict.values():
    inner_lst=[]
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
print(data)
#row_name=          index
col_name=["case_id","avg_cc_score","avg_cc_level","avg_LLOC","avg_unique_operator_Nums","avg_unique_operand_Nums","avg_operator_Nums","avg_operand_Nums","RDI"]
data=pd.DataFrame(data,columns=col_name)
print(1)
print(data)
#去除空行
data.dropna(how='any',inplace=True)
print()
#数据探索
print(2)
print(data.describe())
print()

#特征选择
features=["avg_cc_score","avg_cc_level","avg_LLOC","avg_unique_operator_Nums","avg_unique_operand_Nums","avg_operator_Nums","avg_operand_Nums"]
features_data=data[features]
print(3)
print(features_data)
print()
labels_data=data["RDI"]
print(4)
print(labels_data)
print()

#划分训练集 测试集
train_features,test_features,train_labels,test_labels=train_test_split(features_data,labels_data,test_size=0.3,random_state=0)
print(5)
print(train_features)
print()
print(6)
print(train_labels)
print()

dvec=DictVectorizer(sparse=False)
#得到转化后的训练集的特征值矩阵
train_features=dvec.fit_transform(train_features.to_dict('record'))
print('转换后的特征属性',dvec.feature_names_)

#id3
#clf=DecisionTreeClassifier(criterion='entropy')
clf=DecisionTreeClassifier()
clf.fit(train_features,train_labels)

#决策树可视化  必须在fit后执行，在predict之后运行会报错
import graphviz
from sklearn import tree
dot_data=tree.export_graphviz(clf,feature_names=dvec.feature_names_,filled=True)
graph=graphviz.Source(dot_data)
graph.render("tree")

#得到转换后的测试集的特征值矩阵
test_features=dvec.transform(test_features.to_dict(orient='record'))
pred_labels=clf.predict(test_features)
score=accuracy_score(test_labels,pred_labels)
#print("ID3决策树准确率 %.4lf" % score)
print("CART分类树准确率 %.4lf" % score)

