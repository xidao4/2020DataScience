import json
import numpy as np

def path_msg(case_id):
    global pro_dict
    case = pro_dict[case_id]
    if (case["ans_is_py"]):
        print("path_idx:答案代码", case["path_idx"])
    elif len(case["full_records"])!=0:
        print("path_idx:提交代码", case["full_records"][0])
    else:
        print("答案非py，且没有满分的提交记录","case_id",case_id,"path_idx",case["path_idx"])

def get_cc(case_id):
    try:
        f=open("metrics//"+case_id+"//cc//cc.json",encoding="utf8")
        res = f.read()
        dict = json.loads(res)
    except Exception as e:
        print("打开.json文件失败",e)
        return -1,-1
    cc_lst=[]
    try:
        for v in dict.values():
            # print(v)
            for item in v:
                # print(item)
                s=item["complexity"]
                cc_lst.append(s)
    except Exception as e:
        print("dict",dict)
        print("radon获取圈复杂度失败，仅得到error",e)
    #处理源码之前可能遇到的问题
    if len(cc_lst)==0:
        print("dict",dict)
        print("cc为空")
        return -1,-1
    global cc_suc
    avg_cc_score=np.mean(cc_lst)
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
        avg_cc_level="-1"
        print(case_id," avg_cc_score",avg_cc_score,"圈复杂度分数错误，生成等级失败！")
    cc_suc+=1
    return avg_cc_score,avg_cc_level

def get_raw(case_id):
    try:
        f = open("metrics//" + case_id + "//LLOC//raw.json", encoding="utf8")
        res = f.read()
        dict = json.loads(res)
    except Exception as e:
        print("打开.json文件失败",e)
        return -1
    for v in dict.values():
        try:
            return v["lloc"]
        except Exception as e:
            print("获取raw度量LLOC失败！",v,e)
            return -1

def get_hal(case_id):
    try:
        f=open("metrics//"+case_id+"//hal//hal.json",encoding="utf8")
        res=f.read()
        dict=json.loads(res)
    except Exception as e:
        print("打开.json文件失败", e)
        return -1,-1,-1,-1
    for v in dict.values():
        try:
            return v["total"][0],v["total"][1],v["total"][2],v["total"][3]
        except Exception as e:
            print("获取hal度量失败！",v,e)
            return -1,-1,-1,-1


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

    tmp_lst=get_cc(k)
    inner_dict["avg_cc_score"]=tmp_lst[0]
    print("avg_cc_score", tmp_lst[0])
    inner_dict["avg_cc_level"] = tmp_lst[1]
    print("avg_cc_level", tmp_lst[1])
    inner_dict["avg_LLOC"]=get_raw(k)
    print("avg_LLOC",inner_dict["avg_LLOC"])
    hal_lst=get_hal(k)
    print("hal_lst",hal_lst)
    inner_dict["avg_unique_operator_Nums"]=hal_lst[0]
    inner_dict["avg_unique_operand_Nums"] = hal_lst[1]
    inner_dict["avg_operator_Nums"] = hal_lst[2]
    inner_dict["avg_operand_Nums"]=hal_lst[3]

    diff_dict[k]=inner_dict
    print()
print("成功获取圈复杂度的次数（不是error且不为空）",cc_suc)
print("总题数",len(old_dict))


json_difficulty=json.dumps(diff_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
#要加encoding="utf8" 否则输出到.json中中文乱码
with open('s_difficulty_dict_with_metrics.json',mode='w',encoding="utf8") as f:
    f.write(json_difficulty)

