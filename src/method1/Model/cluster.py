import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import calinski_harabasz_score

def get_data1():
    # 数据加载
    f = open("../PDI/d_difficulty_dict_with_metrics_2.json", encoding="utf8")
    res = f.read()
    diff_dict = json.loads(res)
    data = []
    for v in diff_dict.values():
        inner_lst = []
        inner_lst.append(int(v["case_id"]))
        inner_lst.append(v["avg_cc_score"])
        # 将cc_score与LLOC从字符串转换为float
        if v['avg_cc_level']!=None:
            inner_lst.append(float(v["avg_cc_level"]))
        else:
            inner_lst.append(v["avg_cc_level"])
        if v['avg_LLOC']!=None:
            inner_lst.append(float(v["avg_LLOC"]))
        else:
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
    # 去除RDI为D的行
    data.drop(data[data.RDI == 'D'].index, inplace=True)
    print('去除RDI为D的行后的dataframe')
    print(data)
    return data

def draw_with_classification(y,data,centers):
    print(data)
    print(data.describe())
    # arr0=0
    # arr1=0
    # arr2=0
    # arr3=0
    fig = plt.figure(figsize=(10, 6))
    ax = Axes3D(fig)
    for i in range(len(y)):
        if y[i]==0:
            ax.scatter(data.iloc[i,0], data.iloc[i,1], data.iloc[i,2],c='r', marker='.')
        elif y[i]==1:
            ax.scatter(data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2],c='y', marker='x')
        elif y[i]==2:
            ax.scatter(data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2], c='g', marker='*')
        else:
            print('error')
    ax.scatter(centers[:,0],centers[:,1],centers[:,2],c='b',marker='+')
    # ax=fig.add_subplot(1,1,1)
    # ax=fig.gca(projection='3d')
    plt.title('kmeans scatter result')
    ax.set_xlabel('avg_cc_score')
    ax.set_ylabel('avg_LLOC')
    ax.set_zlabel('avg_unique_operand_Nums')
    #plt.legend(loc=2)
    #plt.show()
    plt.savefig('with_classification.png', bbox_inches='tight')
    # ax=Axes3D(fig)
    # ax.set_zlabel('avg_cc_score')
    # ax.set_ylabel('avg_LLOC')
    # ax.set_xlabel('avg_unique_operand_Nums')
    # for i in range(len(y)):
    #     if y[i]==0:
    # plt.savefig('with_classification.png', bbox_inches='tight')

def my_draw(features_data,filename):
    fig = plt.figure(figsize=(10,6))
    # plt.plot(data['avg_cc_score'],data['avg_LLOC'],data['avg_unique_operand_Nums'])
    # plt.xlabel('avg_cc_score')
    # plt.ylabel('avg_LLOC')
    # plt.zlabel('avg_unique_operand_Nums')
    ax = Axes3D(fig)
    x = features_data.loc[:, 'avg_cc_score']
    y = features_data.loc[:, 'avg_LLOC']
    z = features_data.loc[:, 'avg_unique_operand_Nums']
    ax.scatter(x, y, z)
    ax.set_zlabel('avg_cc_score')
    ax.set_ylabel('avg_LLOC')
    ax.set_xlabel('halstead')
    plt.savefig(filename, bbox_inches='tight')

def get_data2(data):
    #根据箱式图，去除异常点
    data=data[data['avg_cc_score']<12]
    data=data[data['avg_LLOC']<50]
    data=data[data['avg_unique_operand_Nums']<35]
    print('去除了离群点')
    print(data)
    my_draw(data,'before_scaler.png')
    return data

def check_abnormal(data):
    #data.drop(['case_id','avg_operator'],axis=1)
    print(data.describe())
    # 画箱式图，去除影响聚类分析的异常点
    fig=plt.figure(figsize=(10,6))
    #初始化三个子图，分布为一行三列
    ax1=fig.add_subplot(1,3,1)
    ax2=fig.add_subplot(1,3,2)
    ax3=fig.add_subplot(1,3,3)
    #绘制箱型图
    ax1.boxplot(data['avg_cc_score'].values)
    ax1.set_xlabel('avg_cc_score')
    ax2.boxplot(data['avg_LLOC'].values)
    ax2.set_xlabel('avg_LLOC')
    ax3.boxplot(data['avg_unique_operand_Nums'].values)
    ax3.set_xlabel('avg_unique_operand_Nums')
    plt.show()



# def get_features_data_labels_data(data):
#
#     # 数据探索
#     # print(2)
#     # print(data.describe())
#     # print()
#     features = ["avg_cc_score", "avg_LLOC","avg_unique_operand_Nums"]# 特征选择
#     features_data = data[features]
#     # # 写得有问题
#     # features_data.loc[:, 'halstead'] = features_data.apply(total_halstead, axis=1)
#
#     #features_data = features_data.drop(["avg_unique_operator_Nums", "avg_operator_Nums", "avg_operand_Nums"], axis=1)
#     print('最终选择的特征数据')
#     print(features_data)
#     labels_data = data["RDI"]
#     print('所选的特征数据对应结果')
#     print(labels_data)
#     return features_data,labels_data
def kmeans(features_data):
    #标准化 preprocessing.scale
    # 归一化 min-max-scaler
    features_data=features_data.drop(['case_id','avg_cc_level','RDI','avg_unique_operator_Nums','avg_operand_Nums','avg_operator_Nums'],axis=1)
    min_max_scaler=preprocessing.MinMaxScaler()
    features_data = min_max_scaler.fit_transform(features_data)
    print('刚归一化后的原始数据')
    print(features_data)
    features_data = pd.DataFrame(features_data, columns=['avg_cc_score', 'avg_LLOC', 'avg_unique_operand_Nums'])
    print('归一化后转换为dataframe的特征数据')
    print(features_data)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    my_draw(features_data,'after_scaler.png')

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features_data)
    predict_y = kmeans.predict(features_data)
    print('KMeans', calinski_harabasz_score(features_data, predict_y))
    centers=kmeans.cluster_centers_
    print(centers)

    draw_with_classification(predict_y,features_data,centers)


if __name__=='__main__':
    # features_data=get_features_data_labels_data()[0]
    # print('数据归一前')
    # print(features_data)
    # kmeans(features_data)
    data=get_data1() #去除D等级点
    #check_abnormal(data)
    data=get_data2(data) #去除了异常点，还未归一化处理
    kmeans(data)
