import matplotlib.pyplot as plt
#import seaborn as sns
#import pandas as pd
import json

'''
绘制各software metrics与题目平均得分的散点图
'''

if __name__=='__main__':
    f=open("../PDI/d_difficulty_dict_with_metrics_2.json",encoding="utf8")
    res=f.read()
    diff_dict=json.loads(res)

    #matplotlib
    cc_score=[]
    cc_lvl=[]
    LLOC=[]
    u_rator=[]
    u_rand=[]
    rator=[]
    rand=[]
    RDI=[]
    avg_score=[]
    halstead=[]
    for v in diff_dict.values():
        cc_score.append(v["avg_cc_level"])
        #修改：cc_score.append(v['avg_cc_score'])
        LLOC.append(v["avg_LLOC"])
        u_rator.append(v["avg_unique_operator_Nums"])
        u_rand.append(v["avg_unique_operand_Nums"])
        rator.append(v["avg_operator_Nums"])
        rand.append(v["avg_operand_Nums"])
        #RDI.append(v["RDI"])
        avg_score.append(v['avg_score'])
    for i in range(len(cc_score)):
        if cc_score[i]==None:
            continue
        cc_score[i]=float(cc_score[i])
    for i in range(len(LLOC)):
        if LLOC[i] == None:
            continue
        LLOC[i] = float(LLOC[i])
    plt.scatter(avg_score,cc_score)
    plt.show()
    plt.scatter(avg_score,LLOC)
    plt.show()
    # plt.scatter(avg_score,u_rator)
    # plt.show()
    plt.scatter(avg_score,u_rand)
    plt.show()
    # plt.scatter(avg_score,rator)
    # plt.show()
    # plt.scatter(avg_score,rand)
    # plt.show()
    # plt.scatter(halstead, avg_score)
    # plt.show()