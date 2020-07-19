import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import calinski_harabasz_score

'''
kmeans无监督学习：
    数据归一化
    去除异常离群点
    对n_clusters参数进行择优
    评估模型
    可视化
'''

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
        #修改：inner_lst.append(v["avg_cc_level"])
        # 将cc_score与LLOC从字符串转换为float
        # 修改：把下面这个if else中的avg_cc_level改为avg_cc_score
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
    fig = plt.figure(figsize=(10, 6))
    ax = Axes3D(fig)
    for i in range(len(y)):
        if y[i]==0:
            ax.scatter(data.iloc[i,0], data.iloc[i,1], data.iloc[i,2],c='b', marker='.')
        elif y[i]==1:
            ax.scatter(data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2],c='y', marker='x')
        elif y[i]==2:
            ax.scatter(data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2], c='g', marker='*')
        else:
            print('error')
    ax.scatter(centers[:,0],centers[:,1],centers[:,2],c='r',marker='+')
    plt.title('kmeans scatter result')
    ax.set_xlabel('avg_cc_score')
    ax.set_ylabel('avg_LLOC')
    ax.set_zlabel('avg_unique_operand_Nums')
    plt.savefig('with_classification.png', bbox_inches='tight')


def my_draw(features_data,filename):
    fig = plt.figure(figsize=(10,6))
    ax = Axes3D(fig)
    x = features_data.loc[:, 'avg_cc_score']
    y = features_data.loc[:, 'avg_LLOC']
    z = features_data.loc[:, 'avg_unique_operand_Nums']
    ax.scatter(x, y, z)
    ax.set_xlabel('avg_cc_score')
    ax.set_ylabel('avg_LLOC')
    ax.set_zlabel('avg_unique_operand_Nums')
    plt.savefig(filename, bbox_inches='tight')

def get_data2(data):
    #根据箱式图，去除异常点
    data=data[data['avg_cc_score']<12]
    data=data[data['avg_LLOC']<50]
    data=data[data['avg_unique_operand_Nums']<35]
    print('去除了离群点')
    print(data)
    #my_draw(data,'before_scaler.png')
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


    my_draw(features_data,'after_scaler.png')


    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features_data)
    predict_y = kmeans.predict(features_data)
    print('KMeans', calinski_harabasz_score(features_data, predict_y))
    centers=kmeans.cluster_centers_
    print(centers)

    draw_with_classification(predict_y,features_data,centers)


if __name__=='__main__':

    # 1、根据散点图可知，D等级点各软件指标不确定性大，故去除D等级点
    data=get_data1()

    #2、绘制所选特征的箱式图，以便去除异常离群点↓
    #check_abnormal(data)

    # 3、去除了异常点，但还未归一化处理
    data=get_data2(data)

    # 4、
    #归一化处理数据，使之处于0-1之间
    #调整参数n_clusters，比较calinski_harabasz_score。最终选择得分最大的n_clusters为3
    #聚类并可视化，显示质心。
    #由输出的质心坐标，
    #  （XYZ轴分别为答案与满分代码的平均Cyclomatic complexity,logical Source Lines Of Code，unique operand numbers），
    #   可将题目分为ABC三个难度等级
    kmeans(data)
