import json
import numpy as np
import os
import math

def path_msg(case_id):
    global pro_dict
    case = pro_dict[case_id]
    if (case["ans_is_py"]):
        print("path_idx:答案代码", case["path_idx"])
    elif len(case["full_records"])!=0:
        print("path_idx:提交代码", case["full_records"])
    else:
        print("答案非py，且没有满分的提交记录","case_id",case_id,"path_idx",case["path_idx"])


def get_avg_cc(case_id): #获取平均cc
    try:
        all_cc_score=[]
        all_cc_level=[]
        # f=open("metrics//"+case_id+"//cc",encoding="utf8")
        path="metrics//"+case_id+"//cc"
        count=0
        for file in os.listdir(path):      #统计cc文件下有多少个cc.json文件
            count+=1

        for i in range(0,count):           #遍历全部算一遍
            res=get_cc(case_id,i)
            all_cc_score.append(res[0])
            all_cc_level.append(res[1])
        level_to_num=[]
        for j in all_cc_level:
            level_to_num.append(ord(j)-64)
        avg_level=np.mean(level_to_num)
        avg_level=chr(math.ceil(round(avg_level)+64))  #levcl转换数字求平均
        #a=np.mean(all_cc_level)  #这样用会报错
        a=format(sum(all_cc_score)/count,'.1f')   #笨方法求和平均
        global cc_suc
        cc_suc += 1
        return avg_level,a   #返回平均值
    except Exception as e:
        print("打开cc文件失败",e)
        return

def get_avg_raw(case_id): #求平均raw
    try:
        all_lloc_raw=[]
        # f = open("metrics//" + case_id + "//LLOC", encoding="utf8")
        path = "metrics//" + case_id + "//LLOC"
        count=0
        for file in os.listdir(path):
            count+=1
        for i in range(0,count):
            all_lloc_raw.append(get_raw(case_id,i))
        return np.mean(all_lloc_raw)
    except Exception as e:
        print("打开LLOC文件失败", e)
        return

def get_avg_hal(case_id):#求平均hal
    try:
        all_lloc_hal=[]
        # f = open("metrics//" + case_id + "//hal", encoding="utf8")
        path = "metrics//" + case_id + "//hal"
        count=0
        for file in os.listdir(path):
            count+=1
        for i in range(0,count):
            all_lloc_hal.append(get_hal(case_id,i))
        return np.mean(all_lloc_hal,axis=0)
    except Exception as e:
        print("打开hal文件失败", e)
        return



def get_cc(case_id,indexof_ccjson):
    try:
        f=open("metrics//"+case_id+"//cc//cc"+str(indexof_ccjson)+".json",encoding="utf8")
        res = f.read()
        dict = json.loads(res)
    except Exception as e:
        print("打开.json文件失败",e)
        return
    cc_lst=[]
    try:
        for v in dict.values():
            # print(v)
            for item in v:
                # print(item)
                s=item["complexity"]
                cc_lst.append(s)
                for temp in item["closures"]:     #加上子方法的complexity
                    cc_lst.append(temp["complexity"])

    except Exception as e:
        print("dict",dict)
        print("radon获取圈复杂度失败，仅得到error",e)
    #处理源码之前可能遇到的问题
    if len(cc_lst)==0:
        print("dict",dict)
        print("cc为空")
        return
    global cc_suc
    avg_cc_score=np.mean(cc_lst)    #去平均
    avg_cc_level=None
    if 1<=avg_cc_score and avg_cc_score<5.5:
        avg_cc_level="A"
    elif 5.5 <= avg_cc_score and avg_cc_score < 10.5:
        avg_cc_level = "B"
    elif 10.5 <= avg_cc_score and avg_cc_score < 20.5:
        avg_cc_level = "C"
    elif 20.5 <= avg_cc_score and avg_cc_score < 30.5:
        avg_cc_level = "D"
    elif 30.5 <= avg_cc_score and avg_cc_score < 40.5:
        avg_cc_level = "E"
    elif 40.5 <= avg_cc_score:
        avg_cc_level = "F"
    else:
        print(case_id," avg_cc_score",avg_cc_score,"圈复杂度分数错误，生成等级失败！")

    return avg_cc_score,avg_cc_level

def get_raw(case_id,indexof_rawjson):
    try:
        f = open("metrics//" + case_id + "//LLOC//raw"+str(indexof_rawjson)+".json", encoding="utf8")
        res = f.read()
        dict = json.loads(res)
    except Exception as e:
        print("打开.json文件失败",e)
        return
    for v in dict.values():
        try:
            return v["lloc"]
        except Exception as e:
            print("获取raw度量LLOC失败！",v,e)
            return

def get_hal(case_id,indexof_haljson):
    try:
        f=open("metrics//"+case_id+"//hal//hal"+str(indexof_haljson)+".json",encoding="utf8")
        res=f.read()
        dict=json.loads(res)
    except Exception as e:
        print("打开.json文件失败", e)
        return []
    for v in dict.values():
        try:
            return v["total"][0],v["total"][1],v["total"][2],v["total"][3]
        except Exception as e:
            print("获取hal度量失败！",v,e)
            return []


f=open("s_pro_detail_dict.json",encoding="utf8")
res=f.read()
pro_dict=json.loads(res)
f=open("s_difficulty_dict.json",encoding="utf8")
res=f.read()
old_dict=json.loads(res)

diff_dict={}
cc_suc=0
for k in pro_dict.keys():
    inner_dict={}
    inner_dict["case_id"]=k
    print("case_id",k)
    path_msg(k)
    old_case=old_dict[k]
    inner_dict["case_type"]=old_case["case_type"]
    inner_dict["RDI"]=old_case["RDI"]

    tmp_lst=get_avg_cc(k)
    if tmp_lst !=None:
        inner_dict["avg_cc_score"]=tmp_lst[0]
        inner_dict["avg_cc_level"] = tmp_lst[1]
    else:
        inner_dict["avg_cc_score"] = None
        inner_dict["avg_cc_level"] = None
    print("avg_cc_score_level", tmp_lst)

    ret=format(get_avg_raw(k),'.1f')
    if ret!=None:
        inner_dict["avg_LLOC"]=ret
    else:
        inner_dict["avg_LLOC"]=None
    print("avg_LLOC",inner_dict["avg_LLOC"])


    hal_lst=get_avg_hal(k)
    if hal_lst!=[]:
        for i in range(0,len(hal_lst)):
            hal_lst[i]=math.ceil(round(hal_lst[i]))
    if hal_lst!=[]:   #判断None改为[]
        inner_dict["avg_unique_operator_Nums"]=hal_lst[0]
        inner_dict["avg_unique_operand_Nums"] = hal_lst[1]
        inner_dict["avg_operator_Nums"] = hal_lst[2]
        inner_dict["avg_operand_Nums"]=hal_lst[3]
    else:
        inner_dict["avg_unique_operator_Nums"] =None
        inner_dict["avg_unique_operand_Nums"] = None
        inner_dict["avg_operator_Nums"] = None
        inner_dict["avg_operand_Nums"] = None
    print("hal_lst", hal_lst)

    diff_dict[k]=inner_dict
    print()
print("成功获取圈复杂度的次数（不是error且不为空）",cc_suc)
print("总题数",len(old_dict))


json_difficulty=json.dumps(diff_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
#要加encoding="utf8" 否则输出到.json中中文乱码
with open('s_difficulty_dict_with_metrics.json',mode='w',encoding="utf8") as f:
    f.write(json_difficulty)

