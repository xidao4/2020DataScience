### **运行顺序：**

#### Preprocessing:
##### 预处理
preprocess.py -> pro_basic_info.py
##### 分离正常和异常样本，抽取样本进行准确率检测
sample_separator.py -> random_50+50_sample.py -> get_50+50_file.py
##### 数据可视化
student_TO_visiable.py -> to_visiable.py

#### PDI:
cmd_command.py 生成 get_metrics.bat 运行 get_metrics.bat -> collect_metrics.py
modify.py

#### RDI:
get_RDI.py

#### Model:
relation_explore.py -> classification.py -> cluster.py 


### 各文件主要功能与重要方法功能

#### 1、preprocess.py
采用给定的数据集test_data.json，检测异常提交，包括面向用例和非python语言提交
##### check_TO
判断面向用例
##### check_py
判断非python语言

#### 2、pro_basic_info.py
将面向用例和非python语言的提交得分设为0，使每道题的得分更接近真实情况

#### 3、get_50+50_sample.py
从生成的正常样本集和异常样本集中随机抽样进行人工检查，计算检出率和误诊率

#### 4、to_visiable.py
对面向对象的提交记录数据情况进行可视化

#### 5、get_RDI.py
根据题目平均得分计算RDI作为真实难度度量

#### 6、PDI
对于每一道题，使用逻辑代码行数，圈复杂度，不同操作符数量这三个维度作为特征，进行数据清洗和预处理
##### collect_metrics.py

#### 7、Model
分别使用无监督学习——聚类分析和有监督学习——AdoBoost分类两种方法创建PDI模型
##### relation_explore.py
绘制各项特征与题目平均得分的散点图

##### classification.py
adoboost分类器
###### param()
对AdoBoost框架学习器个数进行择优
###### param2()
对AdoBoost所集成的弱分类树的深度进行择优

##### cluster.py 
kmeans无监督学习
###### check_abnormal
绘制箱式图去除影响聚类分析的异常点
###### kmeans
归一化处理数据，调整参数，聚类并可视化